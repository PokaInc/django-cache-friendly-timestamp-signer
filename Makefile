.PHONY: deps, test, clean, build

deps:
	pip install -r ./requirements/test.txt

deps-maintainer:
	pip install -r ./requirements/maintainer.txt

test:
	./runtests.py

clean:
	rm -rfv build
	rm -rfv dist
	rm -rfv django_cache_friendly_timestamp_signer.egg-info

build:
	python setup.py sdist

upload: clean build
	twine upload dist/*