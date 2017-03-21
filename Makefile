VERSION=$(shell grep version= setup.py | sed "s/^[ ]*version='//g;s/',$$//g")
TWINE_ARGS=-u $(shell get-user.sh.php -r pypi.python.org.json) -p $(shell get-password.sh.php -r pypi.python.org.json)

$(info VERSION:$(VERSION))
$(info TWINE_ARGS:$(TWINE_ARGS))

.PHONY:
all :

.PHONY :
clean-dist:
	rm dist/*

.PHONY : deploy
deploy: clean-dist sdist
	twine upload $(TWINE_ARGS) dist/*

.PHONY : register
register: sdist
	# twine register $(TWINE_ARGS) dist/nephele-$(VERSION)-py2-none-any.whl
	# twine register $(TWINE_ARGS) dist/nephele-$(VERSION).tar.gz

.PHONY : sdist
sdist:
	python setup.py sdist bdist_wheel

.PHONY : build
build:
	python setup.py build

.PHONY : install
install:
	python setup.py install
