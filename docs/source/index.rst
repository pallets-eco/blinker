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
 - thread safety

Blinker was written by Jason Kirtand and is provided under the MIT
License. The library supports Python 2.4 or later; Python 3.0 or later;
or Jython 2.5 or later; or PyPy 1.6 or later.


Decoupling With Named Signals
-----------------------------

Named signals are created with :func:`signal`:

.. doctest::

  >>> from blinker import signal
  >>> initialized = signal('initialized')
  >>> initialized is signal('initialized')
  True

Every call to ``signal('name')`` returns the same signal object,
allowing unconnected parts of code (different modules, plugins,
anything) to all use the same signal without requiring any code
sharing or special imports.


Subscribing to Signals
----------------------

:meth:`Signal.connect` registers a function to be invoked each time
the signal is emitted.  Connected functions are always passed the
object that caused the signal to be emitted.

.. doctest::

  >>> def subscriber(sender):
  ...     print("Got a signal sent by %r" % sender)
  ...
  >>> ready = signal('ready')
  >>> ready.connect(subscriber)
  <function subscriber at 0x...>


Emitting Signals
----------------

Code producing events of interest can :meth:`Signal.send`
notifications to all connected receivers.

Below, a simple ``Processor`` class emits a ``ready`` signal when it's
about to process something, and ``complete`` when it is done.  It
passes ``self`` to the :meth:`~Signal.send` method, signifying that
that particular instance was responsible for emitting the signal.

.. doctest::

  >>> class Processor:
  ...    def __init__(self, name):
  ...        self.name = name
  ...
  ...    def go(self):
  ...        ready = signal('ready')
  ...        ready.send(self)
  ...        print("Processing.")
  ...        complete = signal('complete')
  ...        complete.send(self)
  ...
  ...    def __repr__(self):
  ...        return '<Processor %s>' % self.name
  ...
  >>> processor_a = Processor('a')
  >>> processor_a.go()
  Got a signal sent by <Processor a>
  Processing.

Notice the ``complete`` signal in ``go()``?  No receivers have
connected to ``complete`` yet, and that's a-ok.  Calling
:meth:`~Signal.send` on a signal with no receivers will result in no
notifications being sent, and these no-op sends are optimized to be as
inexpensive as possible.


Subscribing to Specific Senders
-------------------------------

The default connection to a signal invokes the receiver function when
any sender emits it.  The :meth:`Signal.connect` function accepts an
optional argument to restrict the subscription to one specific sending
object:

.. doctest::

  >>> def b_subscriber(sender):
  ...     print("Caught signal from processor_b.")
  ...     assert sender.name == 'b'
  ...
  >>> processor_b = Processor('b')
  >>> ready.connect(b_subscriber, sender=processor_b)
  <function b_subscriber at 0x...>

This function has been subscribed to ``ready`` but only when sent by
``processor_b``:

.. doctest::

  >>> processor_a.go()
  Got a signal sent by <Processor a>
  Processing.
  >>> processor_b.go()
  Got a signal sent by <Processor b>
  Caught signal from processor_b.
  Processing.


Sending and Receiving Data Through Signals
------------------------------------------

Additional keyword arguments can be passed to :meth:`~Signal.send`.
These will in turn be passed to the connected functions:

.. doctest::

  >>> send_data = signal('send-data')
  >>> @send_data.connect
  ... def receive_data(sender, **kw):
  ...     print("Caught signal from %r, data %r" % (sender, kw))
  ...     return 'received!'
  ...
  >>> result = send_data.send('anonymous', abc=123)
  Caught signal from 'anonymous', data {'abc': 123}

The return value of :meth:`~Signal.send` collects the return values of
each connected function as a list of (``receiver function``, ``return
value``) pairs:

.. doctest::

  >>> result
  [(<function receive_data at 0x...>, 'received!')]


Anonymous Signals
-----------------

Signals need not be named.  The :class:`Signal` constructor creates a
unique signal each time it is invoked.  For example, an alternative
implementation of the Processor from above might provide the
processing signals as class attributes:

.. doctest::

  >>> from blinker import Signal
  >>> class AltProcessor:
  ...    on_ready = Signal()
  ...    on_complete = Signal()
  ...
  ...    def __init__(self, name):
  ...        self.name = name
  ...
  ...    def go(self):
  ...        self.on_ready.send(self)
  ...        print("Alternate processing.")
  ...        self.on_complete.send(self)
  ...
  ...    def __repr__(self):
  ...        return '<AltProcessor %s>' % self.name
  ...

``connect`` as a Decorator
--------------------------

You may have noticed the return value of :meth:`~Signal.connect` in
the console output in the sections above.  This allows ``connect`` to
be used as a decorator on functions:

.. doctest::

  >>> apc = AltProcessor('c')
  >>> @apc.on_complete.connect
  ... def completed(sender):
  ...     print "AltProcessor %s completed!" % sender.name
  ...
  >>> apc.go()
  Alternate processing.
  AltProcessor c completed!

While convenient, this form unfortunately does not allow the
``sender`` or ``weak`` arguments to be customized for the connected
function.  For this, :meth:`~Signal.connect_via` can be used:

.. doctest::

  >>> dice_roll = signal('dice_roll')
  >>> @dice_roll.connect_via(1)
  ... @dice_roll.connect_via(3)
  ... @dice_roll.connect_via(5)
  ... def odd_subscriber(sender):
  ...     print("Observed dice roll %r." % sender)
  ...
  >>> result = dice_roll.send(3)
  Observed dice roll 3.


Optimizing Signal Sending
-------------------------

Signals are optimized to send very quickly, whether receivers are
connected or not.  If the keyword data to be sent with a signal is
expensive to compute, it can be more efficient to check to see if any
receivers are connected first by testing the :attr:`~Signal.receivers`
property:

.. doctest::

  >>> bool(signal('ready').receivers)
  True
  >>> bool(signal('complete').receivers)
  False
  >>> bool(AltProcessor.on_complete.receivers)
  True

Checking for a receiver listening for a particular sender is also
possible:

.. doctest::

  >>> signal('ready').has_receivers_for(processor_a)
  True


Documenting Signals
-------------------

Both named and anonymous signals can be passed a ``doc`` argument at
construction to set the pydoc help text for the signal.  This
documentation will be picked up by most documentation generators (such
as sphinx) and is nice for documenting any additional data parameters
that will be sent down with the signal.

See the documentation of the :obj:`receiver_connected` built-in signal
for an example.


API Documentation
-----------------

All public API members can (and should) be imported from ``blinker``::

  from blinker import ANY, signal

.. currentmodule:: blinker.base

Basic Signals
+++++++++++++

.. autodata:: blinker.base.ANY

.. autodata:: blinker.base.receiver_connected

.. autoclass:: Signal
   :members:
   :undoc-members:

Named Signals
+++++++++++++

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

.. autoclass:: WeakNamespace
   :show-inheritance:
   :members: signal


.. include:: ../../CHANGES

