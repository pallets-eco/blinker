try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

readme = open('README.rst').read()
import blinker
version = blinker.__version__

setup(name="blinker",
      version=version,
      packages=['blinker'],
      author='Jason Kirtland',
      author_email='jek@discorporate.us',
      maintainer="Pallets Ecosystem",
      maintainer_email="contact@palletsprojects.com",
      description='Fast, simple object-to-object and broadcast signaling',
      keywords='signal emit events broadcast',
      long_description=readme,
      long_description_content_type="text/x-rst",
      license='MIT License',
      url='https://blinker.readthedocs.io',
      project_urls={
        'Source': 'https://github.com/pallets-eco/blinker',
      },
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries',
          ],
)
