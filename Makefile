init-env:
	pip install . --no-cache-dir

init-dev:
	pip install -e ".[all]" --no-cache-dir
	pre-commit install

clean-notebooks:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/*.ipynb

clean-folders:
	rm -rf .ipynb_checkpoints __pycache__ .pytest_cache */.ipynb_checkpoints */__pycache__ */.pytest_cache
	rm -rf site build dist htmlcov .coverage .tox .mypy_cache

interrogate:
	interrogate -vv --ignore-nested-functions --ignore-module --ignore-init-method --ignore-private --ignore-magic --ignore-property-decorators --fail-under=90 deczoo tests

style:
	black --target-version py310 --line-length 90 --workers 4 deczoo tests
	isort --profile black -l 90 deczoo tests
	ruff deczoo tests


test:
	pytest tests -n auto

test-coverage:
	rm -rf .coverage
	coverage run -m pytest
	coverage report -m
	coverage-badge -o docs/img/coverage.svg

check: interrogate style test clean-folders

docs-serve:
	mkdocs serve

docs-deploy:
	mkdocs gh-deploy

pypi-push:
	python -m pip install twine wheel --no-cache-dir

	python setup.py sdist
	python setup.py bdist_wheel --universal
	twine upload dist/*

interrogate-badge:
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method  --generate-badge docs/img/interrogate-shield.svg
