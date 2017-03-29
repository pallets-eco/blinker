try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.md').read()

def find_version(*file_paths):
    """
    Don't pull version by importing package as it will be broken due to as-yet uninstalled
    dependencies, following recommendations at  https://packaging.python.org/single_source_version,
    extract directly from the init file
    """
    import os
    import re
    import io
    def read(*names, **kwargs):
        with io.open(
                os.path.join(os.path.dirname(__file__), *names),
                encoding=kwargs.get("encoding", "utf8")
        ) as fp:
            return fp.read()

    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

version = find_version("blinker", "__init__.py")


requirements = ['orderedset>=1.1.1']
import sys
if sys.version_info < (2, 7):
    requirements += ['ordereddict>=1.1']

setup(name="blinker",
      version=version,
      packages=['blinker'],
      author='Jason Kirtland',
      author_email='jek@discorporate.us',
      description='Fast, simple object-to-object and broadcast signaling',
      keywords='signal emit events broadcast',
      long_description=readme,
      license='MIT License',
      url='http://pythonhosted.org/blinker/',
      install_requires=requirements,
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
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities',
          ],
)
