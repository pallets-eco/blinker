TIP=$(shell hg tip --template '{rev}')
REL=$(shell python -c 'import blinker; print blinker.__version__')

release:
	@echo Preparing blinker release $(REL)
	(cd docs/source && make clean)
	(cd docs/source && make doctest)
	(cd docs/source && VERSION=$(REL) make html)
	(cd docs/source && VERSION=$(REL) make text)
	python setup.py sdist --formats=zip

tip-sdist:
	@echo "Preparing sdist of blinker @ hg.$(TIP)"
	perl -pi -e \
          "s~version = blinker.__version__~version = 'hg.$(TIP)'~" \
          setup.py
	(cd docs/source && make clean)
	(cd docs/source && VERSION=$(TIP) make html)
	(cd docs/source && VERSION=$(TIP) make text)
	python setup.py sdist
	perl -pi -e \
          "s~version = 'hg.$(TIP)'~version = blinker.__version__~" \
          setup.py
