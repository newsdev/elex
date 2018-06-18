.PHONY: test

test:
	flake8 elex
	flake8 tests
	make -C docs html
	python -m nose2.__main__ -v
