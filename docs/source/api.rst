.. _api:

API Documentation
=================

All public API members can (and should) be imported from ``blinker``::

  from blinker import ANY, signal

.. currentmodule:: blinker.base

Basic Signals
-------------

.. autoattribute:: blinker.base.ANY

.. autoattribute:: blinker.base.receiver_connected

.. autoclass:: Signal
   :members:
   :undoc-members:

Named Signals
-------------

.. function:: signal(name, doc=None)

  Return the :class:`NamedSignal` *name*, creating it if required.

  Repeated calls to this function will return the same signal object.
  Signals are created in a global :class:`Namespace`.

.. autoclass:: NamedSignal
   :show-inheritance:
   :members:

.. autoclass:: Namespace
   :show-inheritance:
   :members: signal
