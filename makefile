PIP=uv pip
PACKAGE=youtube-downloader-cli
CMD=youtube-downloader
WHL=$(wildcard dist/*.whl)
TESTPYPI_INDEX=https://test.pypi.org/simple/
PYPI_INDEX=https://pypi.org/simple/

.PHONY: clean build rebuild init run

run:
	uv run $(CMD)

rebuild: clean
	uv build --refresh

build:
	uv build 

init: clean
	uv sync --refresh --extra dev --no-install-project

clean:
	rm -rf dist/
	rm -rf .venv/
	rm -rf *.egg-info/

upload: rebuild
	twine upload -r pypi dist/*

install:
	uv tool install $(PACKAGE) -U --reinstall

upload-test: rebuild
	twine upload -r testpypi dist/*

install-test:
	uv tool install $(PACKAGE) -U --reinstall --index $(TESTPYPI_INDEX) --index-url $(PYPI_INDEX)

testing: rebuild
	bash -c "source $$(which virtualenvwrapper.sh); \
	mkvirtualenv -i $(WHL) --clear yt-dl-cli-testing"
