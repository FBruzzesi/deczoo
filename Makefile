black:
	black --target-version py38 deczoo

flake:
	flake8 deczoo

test:
	pytest tests

interrogate:
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method --fail-under 80 tests
	interrogate -vv --ignore-nested-functions --ignore-semiprivate --ignore-private --ignore-magic --ignore-module --ignore-init-method --fail-under 80 deczoo

clean-nb:
	jupyter nbconvert --ClearOutputPreprocessor.enabled=True --inplace notebooks/*.ipynb

clean-folders:
	rm -rf .ipynb_checkpoints __pycache__ .pytest_cache */.ipynb_checkpoints */__pycache__ */.pytest_cache

init-env:
	pip install -r requirements.txt --no-cache-dir

init-dev-env:
	init-env
	pip install -r requirements-dev.txt --no-cache-dir

precommit: clean-folders black interrogate clean-nb clean-folders
