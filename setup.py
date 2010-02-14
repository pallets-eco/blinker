"""
blinker
~~~~~~~


"""
from distutils.tools import setup


setup(name="blinker",
      version="0.8",
      packages=['blinker'],
      author='Jason Kirtland',
      author_email='jek@discorporate.us',
      description='fast and simple object-to-object and broadcast signalling',
      keywords='signal emit events broadcast',
      long_description=__doc__,
      license='MIT License',
      url='http://discorporate.us/jek/projects/blinker/',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.4',
          'Programming Language :: Python :: 2.5',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          # 'Programming Language :: Python :: 3.1', # _saferef fails :(
          'Topic :: Software Development :: Libraries'
          'Topic :: Utilities',
          ],
)
