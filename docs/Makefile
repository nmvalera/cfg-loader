# A sample Makefile for facilitating docs building on Boilerplate-Python.

# Docs directory

# Sphinx info
SPHINXOPTS=
SPHINXPROJ=Boilerplate-Python
ROOTDIR=..
SOURCEDIR=.
DOCS_DIR=docs
BUILDDIR=_build

# Sphinx build executable
SPHINX_EXEC_PATH=$(ROOTDIR)/$(EXEC_PATH)
SPHINXBUILD=$(SPHINX_EXEC_PATH)sphinx-build

.PHONY: venv develop init clean-pyc clean-build clean-html clean build-html html

clean:
	@rm -rfv $(BUILDDIR)

build-html:
	@echo "Building docs..."
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)/html
	@echo "Build finished. The HTML pages are in $(BUILDDIR)/html."

html: clean build-html
	@xdg-open $(BUILDDIR)/html/docs/index.html