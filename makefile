SHELL=/usr/bin/bash
PIP=uv pip
PACKAGE=youtube-downloader-cli
CMD=youtube-downloader
WHL=$(shell find dist/ -name '*-any.whl')
TESTPYPI_INDEX=https://test.pypi.org/simple/
PYPI_INDEX=https://pypi.org/simple/


run:
	uv run $(CMD)

format: 
	uv run ruff check --fix
	uv run ruff format

rebuild: clean init-build build

build: format build-uv

build-uv:
	uv build --refresh

init: clean init-tool init-build init-upload

init-build: init-dev

init-dev:
	uv sync --refresh --extra dev --no-install-project

init-upload:
	uv tool install -U twine 

init-tool:
	uv tool install -U bump-my-version 

clean:
	rm -rf dist/
	rm -rf .venv/
	rm -rf *.egg-info/
	rm -rf $$(find -name '__pycache__')

upload: rebuild init-upload
	twine upload -r pypi dist/*

install:
	uv tool install $(PACKAGE) -U --reinstall

upload-test: rebuild init-upload
	twine upload -r testpypi dist/*

install-test:
	uv tool install $(PACKAGE) -U --reinstall --index $(TESTPYPI_INDEX) --index-url $(PYPI_INDEX)

testing: rebuild
	source $$(which virtualenvwrapper.sh); \
	VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 \
	mkvirtualenv -i $(WHL) --clear yt-dl-cli-testing

clean-testing:
	source $$(which virtualenvwrapper.sh); \
	VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3 \
	rmvirtualenv yt-dl-cli-testing

