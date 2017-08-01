VERSION=$(shell grep version= setup.py | sed "s/^[ ]*version='//g;s/',$$//g")
TWINE_ARGS=-u $(shell get-user.sh.php -r pypi.python.org.json) -p $(shell get-password.sh.php -r pypi.python.org.json)

$(info VERSION:$(VERSION))
$(info TWINE_ARGS:$(TWINE_ARGS))

.PHONY:
all :

.PHONY : clean
clean:
	python setup.py clean
	rm -rf /usr/local/lib/python2.7/site-packages/nephele-0.0.*
	rm -rf dist/*
	rm -rf build/*
	rm -rf nephele.egg-info

.PHONY : deploy
deploy: clean install
	twine upload $(TWINE_ARGS) dist/*

.PHONY : sdist
sdist:
	python setup.py sdist bdist_wheel

.PHONY : test
test :
	python setup.py develop
	python setup.py nosetests -s

.PHONY : build
build: test sdist
	python setup.py build


.PHONY : install
install: build
	python setup.py install

.PHONY : run
run: 
	cd nephele && ./main.py
