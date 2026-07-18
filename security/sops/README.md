# SOPS + age 密钥工作流

本目录实现 [ADR-009](../../docs/adr/ADR-009-使用SOPS与age管理密钥.md)。仓库只保存 age 公钥 recipient、SOPS 规则、密文和无敏感值模板；禁止保存 age identity。

## 1. 工具版本

- SOPS `3.13.0`
- age `1.3.1`

升级工具前必须在 Windows、macOS、Linux 验证加密、解密和重新加密。

## 2. 首次初始化

每个环境单独生成 identity：

```bash
age-keygen -o age-local-identity.txt
age-keygen -o age-dev-identity.txt
age-keygen -o age-test-identity.txt
age-keygen -o age-prod-like-identity.txt
```

命令会输出对应公钥，例如 `age1...`。只把公钥写入从 `.sops.yaml.example` 复制生成的 `.sops.yaml`；identity 文件不得进入仓库。

Windows PowerShell：

```powershell
$env:SOPS_AGE_KEY_FILE = 'C:\secure\mom-infra\age-local-identity.txt'
```

Linux/macOS：

```bash
export SOPS_AGE_KEY_FILE="$HOME/.config/mom-infra/age-local-identity.txt"
```

## 3. 加密

明文模板只能在仓库外或临时目录中填写：

```bash
sops --encrypt --config security/sops/.sops.yaml \
  security/sops/templates/postgresql-secret.template.yaml \
  > environments/local/secrets/postgresql-secret.sops.yaml
```

加密后必须检查：

- 敏感字段均为 `ENC[...]`。
- 文件包含顶层 `sops` 元数据。
- Git Diff 不出现可用密码、Token 或私钥。

## 4. 编辑与轮换

直接编辑密文：

```bash
sops environments/local/secrets/postgresql-secret.sops.yaml
```

recipient 轮换：

```bash
sops updatekeys environments/local/secrets/postgresql-secret.sops.yaml
```

轮换后必须确认旧 identity 无法解密，并记录受影响环境、文件和验证证据。

## 5. 解密与部署

解密结果只能通过管道或临时目录使用：

```bash
sops --decrypt environments/local/secrets/postgresql-secret.sops.yaml \
  | kubectl --context <explicit-context> apply -f -
```

禁止：

- 将解密结果写回仓库目录后长期保留。
- 在命令行历史中直接输入明文密码。
- 在 CI 日志中输出解密内容。
- 多环境共用同一个 age identity。

## 6. 恢复要求

age identity 至少保存两份受控备份，并验证：

1. 从备份介质恢复 identity。
2. 解密一份测试密文。
3. 重新加密并验证新旧 recipient 行为。
4. 记录恢复耗时和失败点。

未完成 identity 恢复验证前，Secret 工作流不得标记为 `prod-like-ready`。
