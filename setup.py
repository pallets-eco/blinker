try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    from Cython.Build import cythonize
    extensions = cythonize('blinker/_speedup.pyx')
except ImportError:
    extensions = None

readme = open('README.md').read()
import blinker
version = blinker.__version__

setup(name="blinker",
      version=version,
      packages=['blinker'],
      ext_modules=extensions,
      author='Jason Kirtland',
      author_email='jek@discorporate.us',
      description='Fast, simple object-to-object and broadcast signaling',
      keywords='signal emit events broadcast',
      long_description=readme,
      license='MIT License',
      url='http://pythonhosted.org/blinker/',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.4',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.0',
          'Programming Language :: Python :: 3.1',
          'Programming Language :: Python :: 3.2',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          ],
)
