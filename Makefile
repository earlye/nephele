.PHONY:
all :

.PHONY :
clean:
	rm dist/*

.PHONY : deploy
deploy: build
	twine upload -u $(shell get-user.sh.php -r pypi.python.org.json) -p $(shell get-password.sh.php -r pypi.python.org.json)

.PHONY : sdist
sdist:
	python setup.py sdist bdist_wheel

.PHONY : build
build:
	python setup.py build

.PHONY : install
install:
	python setup.py install
