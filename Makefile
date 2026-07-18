.PHONY: validate render validate-source validate-rendered

validate:
	./scripts/validate.sh

render:
	./scripts/render.sh

validate-source:
	python3 scripts/validate.py --mode source

validate-rendered: render
	python3 scripts/validate.py --mode rendered --rendered-dir .tmp/rendered
