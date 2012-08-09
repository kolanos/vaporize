SHELL := /bin/bash

# these files should pass pyflakes
# exclude ./env/, which may contain virtualenv packages
PYFLAKES_WHITELIST=$(shell find . -name "*.py" ! -path "./docs/*" ! -path "./tests/*" \
	! -path "./requests/packages/*" ! -path "./env/*" \
	! -path "./requests/__init__.py" ! -path "./requests/compat.py")

# hack: if pyflakes is available, set this to the location of pyflakes
# if it's not, e.g., in the Python 3 or PyPy Jenkins environments, set it to
# the location of the no-op `true` command.
PYFLAKES_IF_AVAILABLE=$(shell if which pyflakes > /dev/null ; \
	then which pyflakes; \
	else which true; fi )

# test_requests_ext.py depends on external services, and async doesn't work under Python 3
# Travis/Jenkins should be ensuring that all other tests pass on all supported versions
CI_TESTS=$(shell find ,/ -name "*.py" ! -name "test_requests_ext.py" ! -name "test_requests_async.py")

init:
	python setup.py develop
	pip install -r requirements.txt

test:
	nosetests -w ./

lazy:
	nosetests --with-color -w ./

simple:
	nosetests -w ./

pyflakes:
	pyflakes ${PYFLAKES_WHITELIST}

cipyflakes:
	${PYFLAKES_IF_AVAILABLE} ${PYFLAKES_WHITELIST}

citests:
	nosetests -w ./ --with-xunit --xunit-file=junit-report.xml

ci: citests cipyflakes

travis: citests

# compute statistics of various kinds
lemonade:
	-pyflakes vaporize > violations.pyflakes.txt
	# HTML output will be available in the default location, ./cover/
	nosetests --with-coverage --cover-html --cover-package=vaporize ${CI_TESTS} ./tests/*

site:
	cd docs; make html

clean:
	git clean -Xfd

docs: site
