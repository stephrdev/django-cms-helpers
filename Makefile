.PHONY: clean correct docs tests coverage-html release
.ONESHELL: release

clean:
	rm -fr build/ dist/ htmlcov/ __pycache__
	poetry run make -C docs clean

correct:
	poetry run isort cms_helpers tests
	poetry run black -q cms_helpers tests

docs:
	poetry run make -C docs html

tests_basic:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --ignore=tests/anylink --ignore=tests/filer

tests_anylink:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --ignore=tests/filer

tests_filer:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --ignore=tests/anylink

tests:
	@PYTHONPATH=$(CURDIR):${PYTHONPATH} poetry run pytest --cov --isort --flake8 --black

coverage-html: tests
	poetry run coverage html

release:
	@VERSION=`poetry version -s`
	@echo About to release $${VERSION}
	@echo [ENTER] to continue; read
	git tag -a "$${VERSION}" -m "Version $${VERSION}" && git push --follow-tags
