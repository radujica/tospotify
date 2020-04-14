MODULE := tospotify

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

build:
	@python setup.py sdist

clean:
	rm -rf .pytest_cache .coverage coverage.xml dist tospotify.egg-info build

.PHONY: test
