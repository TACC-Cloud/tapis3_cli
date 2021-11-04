.PHONY: docs docs/requirements.txt

docs: docs-clean docs-autodoc docs-text docs/requirements.txt

docs/requirements.txt:
	cat requirements.txt > docs/requirements.txt
	cat requirements-dev.txt >> docs/requirements.txt

docs-text:
	cd docs && make html && make man

docs-autodoc:
	cd docs && sphinx-apidoc --maxdepth 1 -M -f -o source ../tapis3_cli

docs-clean:
	cd docs && make clean

lint-source:
	pylint tapis3_cli

lint: lint-source

sort-source:
	isort tapis3_cli

sort: sort-source

reformat-source:
	black tapis3_cli

reformat: reformat-source

code-quality: sort reformat
