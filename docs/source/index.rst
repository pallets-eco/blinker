Blinker Documentation
=====================

Blinker provides fast & simple object-to-object and broadcast
signaling for Python objects.

The core of Blinker is quite small but provides powerful features:

 - a global registry of named signals
 - anonymous signals
 - custom name registries
 - permanently or temporarily connected receivers
 - automatically disconnected receivers via weak referencing
 - sending arbitrary data payloads
 - collecting return values from signal receivers


Requirements
------------

Python 2.4 or later.  No other modules are required.

As of Blinker 0.8, Python 3.1 passes all tests except for weakly
binding to instance methods.


License
-------

Blinker is provided under the MIT License.


Contents
--------

.. toctree::
   :maxdepth: 2

   signals
   api


