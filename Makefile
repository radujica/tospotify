MODULE := tospotify

install:
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt

run:
	$(MODULE)

test:
	@pytest

lint:
	@echo "Running Pylint against source and test files..."
	@pylint --rcfile=setup.cfg $(MODULE)
	@echo "Running Flake8 against source and test files..."
	@flake8 --config=setup.cfg $(MODULE)
	@echo "Running Bandit against source files..."
	@bandit -r --ini setup.cfg

build: clean
	@python setup.py sdist bdist_wheel

publish: clean build
	@echo "Checking build..."
	@twine check dist/*
	@echo "Publishing to pypi..."
	@twine upload -r pypi dist/*

clean:
	rm -rf .pytest_cache .coverage coverage.xml dist tospotify.egg-info build
	find . -name __pycache__ -type d -prune -exec rm -rf {} \;

.PHONY: test
