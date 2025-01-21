PIP=uv pip
PACKAGE=youtube-downloader-cli
TESTPYPI_INDEX=https://test.pypi.org/simple/

.PHONY: clean build rebuild init

rebuild: clean
	uv build --refresh

build:
	uv build 

init: clean
	uv sync --refresh

clean:
	rm -rf dist/
	rm -rf .venv/

test:
	uv tool install $(PACKAGE) --index $(TESTPYPI_INDEX) 
