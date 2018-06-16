.PHONY: test

test:
	flake8 elex
	flake8 tests
	python -m nose2.__main__ -v
