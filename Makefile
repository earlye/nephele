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
deploy: clean sdist
	twine upload $(TWINE_ARGS) dist/*

.PHONY : register
register: sdist
	# twine register $(TWINE_ARGS) dist/nephele-$(VERSION)-py2-none-any.whl
	# twine register $(TWINE_ARGS) dist/nephele-$(VERSION).tar.gz

.PHONY : sdist
sdist:
	python setup.py sdist bdist_wheel

.PHONY : build
build: sdist
	python setup.py build


.PHONY : install
install: build
	python setup.py install
