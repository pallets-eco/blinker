# Makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
VERSION      ?= tip
RELEASE      ?= $(VERSION)

# Internal variables.
ALLSPHINXOPTS   = -D version=$(VERSION) -D release=$(RELEASE) \
   -d ../doctrees $(SPHINXOPTS) .

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  html      to make standalone HTML files"
	@echo "  text      to make standalone text files"
	@echo "  sdist     to build documentation for release"
	@echo "  doctest   to run doctests"
	@echo "  pickles   to build pickles"
	@echo "  clean     to remove generated artifacts"

sdist: clean text html

clean:
	for i in doctrees html text doctest pickles website; do \
	    rm -rf ../$$i; \
        done

html:
	mkdir -p ../html ../doctrees _static _template
	$(SPHINXBUILD) -b html $(ALLSPHINXOPTS) ../html
	@echo
	@echo "Build finished. The HTML pages are in ../html."

text:
	mkdir -p ../text ../doctrees
	$(SPHINXBUILD) -b text $(ALLSPHINXOPTS) ../text
	@echo
	@echo "Build finished. The text pages are in ../text."

doctest:
	mkdir -p ../doctrees ../doctest
	$(SPHINXBUILD) -b doctest $(ALLSPHINXOPTS) ../doctest

pickles:
	mkdir -p ../pickles ../doctest
	$(SPHINXBUILD) -b pickle $(ALLSPHINXOPTS) ../pickles

website:
	mkdir -p ../website ../doctrees
	$(SPHINXBUILD) -b discorporate \
           -D html_theme=discorporate \
           $(ALLSPHINXOPTS) ../website
