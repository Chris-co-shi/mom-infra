#!/usr/bin/env python3
"""Cross-platform policy validation for MOM infrastructure manifests."""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ENVIRONMENTS = ("local", "dev", "test", "prod-like")
EXPECTED_NAMESPACES = {
    "mom-system",
    "mom-data",
    "mom-messaging",
    "mom-observability",
    "mom-apps",
}
REQUIRED_PATHS = (
    "config/component-versions.yaml",
    "kubernetes/base/kustomization.yaml",
    "kubernetes/base/namespaces.yaml",
    "environments/local/kustomization.yaml",
    "environments/dev/kustomization.yaml",
    "environments/test/kustomization.yaml",
    "environments/prod-like/kustomization.yaml",
    "docs/adr/ADR-007-环境与集群拓扑.md",
    "docs/adr/ADR-008-第三方组件部署方式.md",
    "docs/adr/ADR-009-使用SOPS与age管理密钥.md",
    "security/sops/README.md",
    "security/sops/.sops.yaml.example",
)
IGNORED_DIRS = {".git", ".tmp", "rendered", "build", "dist", ".terraform"}
PRIVATE_SUFFIXES = {".pem", ".key", ".p12", ".jks", ".age"}
FLOATING_TAGS = {
    "latest",
    "stable",
    "main",
    "master",
    "edge",
    "snapshot",
    "nightly",
    "canary",
    "dev",
}
POLICY_EXCEPTION = "infra.mom.io/policy-exception"
SHA256_DIGEST = re.compile(r"@sha256:[0-9a-fA-F]{64}$")


class ValidationError(Exception):
    """Raised when an infrastructure policy is violated."""


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def iter_source_yaml_files() -> Iterable[Path]:
    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".yaml", ".yml"}:
            continue
        if any(part in IGNORED_DIRS for part in path.relative_to(ROOT).parts):
            continue
        yield path


def load_documents(path: Path) -> list[dict[str, Any]]:
    try:
        with path.open("r", encoding="utf-8") as handle:
            documents = list(yaml.safe_load_all(handle))
    except (OSError, yaml.YAMLError) as exc:
        raise ValidationError(f"{relative(path)}: invalid YAML: {exc}") from exc

    return [document for document in documents if isinstance(document, dict)]


def annotations(document: Mapping[str, Any]) -> Mapping[str, Any]:
    metadata = document.get("metadata")
    if not isinstance(metadata, Mapping):
        return {}
    value = metadata.get("annotations")
    return value if isinstance(value, Mapping) else {}


def has_policy_exception(document: Mapping[str, Any]) -> bool:
    value = annotations(document).get(POLICY_EXCEPTION)
    return isinstance(value, str) and bool(value.strip())


def walk(node: Any, path: tuple[str, ...] = ()) -> Iterable[tuple[tuple[str, ...], Any]]:
    yield path, node
    if isinstance(node, Mapping):
        for key, value in node.items():
            yield from walk(value, path + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, path + (str(index),))


def validate_image_reference(reference: str, *, location: str, require_digest: bool) -> None:
    reference = reference.strip().strip("'\"")
    if not reference or reference.startswith("ENC["):
        return

    if SHA256_DIGEST.search(reference):
        return

    if require_digest:
        raise ValidationError(f"{location}: prod-like image must use sha256 digest: {reference}")

    last_segment = reference.rsplit("/", 1)[-1]
    if ":" not in last_segment:
        raise ValidationError(f"{location}: image must use an explicit tag or digest: {reference}")

    tag = last_segment.rsplit(":", 1)[1].lower()
    if tag in FLOATING_TAGS:
        raise ValidationError(f"{location}: floating image tag is forbidden: {reference}")


def validate_images(document: Mapping[str, Any], *, location: str, require_digest: bool) -> None:
    for node_path, value in walk(document):
        if not node_path:
            continue
        key = node_path[-1]
        if key == "image" and isinstance(value, str):
            validate_image_reference(
                value,
                location=f"{location}:{'.'.join(node_path)}",
                require_digest=require_digest,
            )
        elif key == "newTag" and isinstance(value, str):
            tag = value.strip().strip("'\"").lower()
            if tag in FLOATING_TAGS:
                raise ValidationError(
                    f"{location}:{'.'.join(node_path)}: floating newTag is forbidden: {value}"
                )


def validate_secret(document: Mapping[str, Any], *, location: str) -> None:
    if document.get("kind") != "Secret":
        return

    encrypted = isinstance(document.get("sops"), Mapping)
    for field in ("data", "stringData"):
        values = document.get(field)
        if not isinstance(values, Mapping) or not values:
            continue

        if not encrypted:
            raise ValidationError(f"{location}: Kubernetes Secret {field} must be SOPS encrypted")

        for key, value in values.items():
            if not isinstance(value, str) or not value.startswith("ENC["):
                raise ValidationError(f"{location}: Secret value {field}.{key} is not SOPS ciphertext")


def pod_spec(document: Mapping[str, Any]) -> Mapping[str, Any] | None:
    kind = document.get("kind")
    spec = document.get("spec")
    if not isinstance(spec, Mapping):
        return None

    if kind == "Pod":
        return spec
    if kind == "CronJob":
        value = spec.get("jobTemplate")
        if isinstance(value, Mapping):
            value = value.get("spec")
        if isinstance(value, Mapping):
            value = value.get("template")
        if isinstance(value, Mapping):
            value = value.get("spec")
        return value if isinstance(value, Mapping) else None
    if kind in {"Deployment", "StatefulSet", "DaemonSet", "ReplicaSet", "Job"}:
        value = spec.get("template")
        if isinstance(value, Mapping):
            value = value.get("spec")
        return value if isinstance(value, Mapping) else None
    return None


def validate_workload_security(document: Mapping[str, Any], *, location: str) -> None:
    if has_policy_exception(document):
        return

    spec = pod_spec(document)
    if spec is None:
        return

    for field in ("hostNetwork", "hostPID", "hostIPC"):
        if spec.get(field) is True:
            raise ValidationError(f"{location}: {field}=true requires {POLICY_EXCEPTION}")

    volumes = spec.get("volumes")
    if isinstance(volumes, list):
        for volume in volumes:
            if isinstance(volume, Mapping) and "hostPath" in volume:
                raise ValidationError(f"{location}: hostPath volume requires {POLICY_EXCEPTION}")

    for collection in ("initContainers", "containers", "ephemeralContainers"):
        containers = spec.get(collection)
        if not isinstance(containers, list):
            continue
        for container in containers:
            if not isinstance(container, Mapping):
                continue
            security_context = container.get("securityContext")
            if isinstance(security_context, Mapping) and security_context.get("privileged") is True:
                name = container.get("name", "<unnamed>")
                raise ValidationError(
                    f"{location}: privileged container {name} requires {POLICY_EXCEPTION}"
                )


def validate_rbac(document: Mapping[str, Any], *, location: str) -> None:
    if has_policy_exception(document):
        return

    kind = document.get("kind")
    if kind in {"RoleBinding", "ClusterRoleBinding"}:
        role_ref = document.get("roleRef")
        if isinstance(role_ref, Mapping) and role_ref.get("name") == "cluster-admin":
            raise ValidationError(f"{location}: cluster-admin binding requires {POLICY_EXCEPTION}")

    if kind == "ClusterRole":
        rules = document.get("rules")
        if not isinstance(rules, list):
            return
        for rule in rules:
            if not isinstance(rule, Mapping):
                continue
            api_groups = rule.get("apiGroups")
            resources = rule.get("resources")
            verbs = rule.get("verbs")
            if api_groups == ["*"] and resources == ["*"] and verbs == ["*"]:
                raise ValidationError(
                    f"{location}: unrestricted ClusterRole requires {POLICY_EXCEPTION}"
                )


def validate_document(
    document: Mapping[str, Any], *, location: str, require_digest: bool = False
) -> None:
    validate_images(document, location=location, require_digest=require_digest)
    validate_secret(document, location=location)
    validate_workload_security(document, location=location)
    validate_rbac(document, location=location)


def validate_required_paths() -> None:
    missing = [path for path in REQUIRED_PATHS if not (ROOT / path).is_file()]
    if missing:
        raise ValidationError("missing required files: " + ", ".join(missing))


def validate_private_material() -> None:
    findings: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        parts = path.relative_to(ROOT).parts
        if any(part in IGNORED_DIRS for part in parts):
            continue
        name = path.name.lower()
        if path.suffix.lower() in PRIVATE_SUFFIXES or "age-identity" in name:
            findings.append(relative(path))
    if findings:
        raise ValidationError(
            "private key or identity material must not be committed: " + ", ".join(findings)
        )


def validate_overlay_contracts() -> None:
    for environment in ENVIRONMENTS:
        path = ROOT / "environments" / environment / "kustomization.yaml"
        documents = load_documents(path)
        if len(documents) != 1:
            raise ValidationError(f"{relative(path)}: expected exactly one Kustomization")
        document = documents[0]

        if "namePrefix" in document or "nameSuffix" in document:
            raise ValidationError(f"{relative(path)}: namespace-changing prefixes/suffixes are forbidden")

        resources = document.get("resources")
        if not isinstance(resources, list) or "../../kubernetes/base" not in resources:
            raise ValidationError(f"{relative(path)}: must reference ../../kubernetes/base")

        labels = document.get("labels")
        expected = False
        if isinstance(labels, list):
            for item in labels:
                if not isinstance(item, Mapping):
                    continue
                pairs = item.get("pairs")
                if isinstance(pairs, Mapping) and pairs.get("mom.io/environment") == environment:
                    expected = True
                    break
        if not expected:
            raise ValidationError(
                f"{relative(path)}: must apply mom.io/environment={environment}"
            )


def validate_source() -> None:
    validate_required_paths()
    validate_private_material()
    validate_overlay_contracts()

    for path in iter_source_yaml_files():
        for index, document in enumerate(load_documents(path), start=1):
            validate_document(document, location=f"{relative(path)}#doc{index}")


def validate_rendered(rendered_dir: Path) -> None:
    if not rendered_dir.is_absolute():
        rendered_dir = ROOT / rendered_dir

    for environment in ENVIRONMENTS:
        path = rendered_dir / f"{environment}.yaml"
        if not path.is_file():
            raise ValidationError(f"missing rendered manifest: {path}")

        documents = load_documents(path)
        namespace_names: set[str] = set()
        for index, document in enumerate(documents, start=1):
            validate_document(
                document,
                location=f"{path.relative_to(ROOT)}#doc{index}",
                require_digest=environment == "prod-like",
            )
            if document.get("kind") == "Namespace":
                metadata = document.get("metadata")
                if not isinstance(metadata, Mapping):
                    continue
                name = metadata.get("name")
                if isinstance(name, str):
                    namespace_names.add(name)
                labels = metadata.get("labels")
                env_label = labels.get("mom.io/environment") if isinstance(labels, Mapping) else None
                if env_label != environment:
                    raise ValidationError(
                        f"{path.relative_to(ROOT)}: Namespace {name} lacks "
                        f"mom.io/environment={environment}"
                    )

        if namespace_names != EXPECTED_NAMESPACES:
            missing = sorted(EXPECTED_NAMESPACES - namespace_names)
            unexpected = sorted(namespace_names - EXPECTED_NAMESPACES)
            raise ValidationError(
                f"{path.relative_to(ROOT)}: namespace contract mismatch; "
                f"missing={missing}, unexpected={unexpected}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("source", "rendered"), default="source")
    parser.add_argument("--rendered-dir", default=".tmp/rendered")
    args = parser.parse_args()

    try:
        if args.mode == "source":
            validate_source()
        else:
            validate_rendered(Path(args.rendered_dir))
    except ValidationError as exc:
        print(f"validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"infrastructure {args.mode} policy validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
