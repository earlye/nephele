VERSION=$(shell grep version= setup.py | sed "s/^[ ]*version='//g;s/',$$//g")
TWINE_ARGS=-u $(shell pass dev/pypi.python.org/user) -p $(shell pass dev/pypi.python.org/pass)
PYTHON=$(shell which python3)

$(info PYTHON:$(PYTHON))
$(info VERSION:$(VERSION))
# $(info TWINE_ARGS:$(TWINE_ARGS))

.PHONY:
all :

.PHONY : clean
clean:
	${PYTHON} setup.py clean
	rm -rf /usr/local/lib/python2.7/site-packages/nephele-0.0.*
	rm -rf /usr/local/lib/python3.7/site-packages/nephele-*
	rm -rf dist/*
	rm -rf build/*
	rm -rf nephele.egg-info

.PHONY : deploy
deploy: clean install
	twine upload $(TWINE_ARGS) dist/*

.PHONY : sdist
sdist:
	${PYTHON} setup.py sdist bdist_wheel

.PHONY : test
test :
	${PYTHON} setup.py develop
	${PYTHON} setup.py nosetests -s

.PHONY : build
build: test sdist
	${PYTHON} setup.py build


.PHONY : install
install: build
	${PYTHON} setup.py install

.PHONY : run
run: 
	nephele
