TIP=$(shell hg tip --template '{rev}')
REL=$(shell python -c 'import blinker; print blinker.__version__')
.PHONY: clean sdist tip-sdist clean website docs test


release: clean test docs sdist website
	@echo Preparing blinker release $(REL)
	(cd docs/source && make clean)
	(cd docs/source && make doctest)
	(cd docs/source && VERSION=$(REL) make html)
	(cd docs/source && VERSION=$(REL) make text)
	python setup.py sdist --formats=zip

sdist:
	python setup.py sdist

tip-sdist:
	@echo "Preparing sdist of blinker @ hg.$(TIP)"
	perl -pi -e \
          "s~version = blinker.__version__~version = 'hg.$(TIP)'~" \
          setup.py
	$(MAKE) clean
	$(MAKE) REL=$(TIP) docs
	$(MAKE) sdist
	perl -pi -e \
          "s~version = 'hg.$(TIP)'~version = blinker.__version__~" \
          setup.py
	$(MAKE) clean

clean:
	(cd docs/source && make clean)

website:
	(cd docs/source && VERSION=$(REL) make website)

docs:
	(cd docs/source && VERSION=$(REL) make html)
	(cd docs/source && VERSION=$(REL) make text)


test:
	(cd docs/source && make doctest)
