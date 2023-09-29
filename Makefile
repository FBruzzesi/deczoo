init-env:
	pip install . --no-cache-dir

init-dev:
	pip install -e ".[all-dev]" --no-cache-dir
	pre-commit install

clean-notebooks:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/*.ipynb

clean-folders:
	rm -rf .ipynb_checkpoints __pycache__ .pytest_cache */.ipynb_checkpoints */__pycache__ */.pytest_cache
	rm -rf site build dist htmlcov .coverage .tox .mypy_cache

lint:
	black deczoo tests
	isort deczoo tests
	ruff deczoo tests

test:
	pytest tests -n auto

coverage:
	rm -rf .coverage
	coverage run -m pytest
	coverage report -m
	coverage-badge -o docs/img/coverage.svg

interrogate:
	interrogate deczoo tests

interrogate-badge:
	interrogate --generate-badge docs/img/interrogate-shield.svg

check: lint test clean-folders

docs-serve:
	mkdocs serve

docs-deploy:
	mkdocs gh-deploy

pypi-push:
	rm -rf dist
	python -m pip install twine hatch --no-cache-dir
	hatch build
	twine upload dist/*
