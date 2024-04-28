.. rst-class:: hide-header

Blinker Documentation
=====================

.. image:: _static/blinker-named.png
    :align: center

.. currentmodule:: blinker

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
License. The library supports Python 3.8 or later; or PyPy3.9 or later.


Decoupling With Named Signals
-----------------------------

Named signals are created with :func:`signal`:

.. code-block:: python

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

.. code-block:: python

  >>> def subscriber(sender):
  ...     print(f"Got a signal sent by {sender!r}")
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

.. code-block:: python

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
  ...        return f'<Processor {self.name}>'
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

.. code-block:: python

  >>> def b_subscriber(sender):
  ...     print("Caught signal from processor_b.")
  ...     assert sender.name == 'b'
  ...
  >>> processor_b = Processor('b')
  >>> ready.connect(b_subscriber, sender=processor_b)
  <function b_subscriber at 0x...>

This function has been subscribed to ``ready`` but only when sent by
``processor_b``:

.. code-block:: python

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

.. code-block:: python

  >>> send_data = signal('send-data')
  >>> @send_data.connect
  ... def receive_data(sender, **kw):
  ...     print(f"Caught signal from {sender!r}, data {kw!r}")
  ...     return 'received!'
  ...
  >>> result = send_data.send('anonymous', abc=123)
  Caught signal from 'anonymous', data {'abc': 123}

The return value of :meth:`~Signal.send` collects the return values of
each connected function as a list of (``receiver function``, ``return
value``) pairs:

.. code-block:: python

  >>> result
  [(<function receive_data at 0x...>, 'received!')]


Muting signals
--------------

To mute a signal, as may be required when testing, the
:meth:`~Signal.muted` can be used as a context decorator:

.. code-block:: python

  sig = signal('send-data')
  with sig.muted():
       ...


Anonymous Signals
-----------------

Signals need not be named.  The :class:`Signal` constructor creates a
unique signal each time it is invoked.  For example, an alternative
implementation of the Processor from above might provide the
processing signals as class attributes:

.. code-block:: python

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
  ...        return f'<AltProcessor {self.name}>'
  ...

``connect`` as a Decorator
--------------------------

You may have noticed the return value of :meth:`~Signal.connect` in
the console output in the sections above.  This allows ``connect`` to
be used as a decorator on functions:

.. code-block:: python

  >>> apc = AltProcessor('c')
  >>> @apc.on_complete.connect
  ... def completed(sender):
  ...     print f"AltProcessor {sender.name} completed!"
  ...
  >>> apc.go()
  Alternate processing.
  AltProcessor c completed!

While convenient, this form unfortunately does not allow the
``sender`` or ``weak`` arguments to be customized for the connected
function.  For this, :meth:`~Signal.connect_via` can be used:

.. code-block:: python

  >>> dice_roll = signal('dice_roll')
  >>> @dice_roll.connect_via(1)
  ... @dice_roll.connect_via(3)
  ... @dice_roll.connect_via(5)
  ... def odd_subscriber(sender):
  ...     print(f"Observed dice roll {sender!r}.")
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

.. code-block:: python

  >>> bool(signal('ready').receivers)
  True
  >>> bool(signal('complete').receivers)
  False
  >>> bool(AltProcessor.on_complete.receivers)
  True

Checking for a receiver listening for a particular sender is also
possible:

.. code-block:: python

  >>> signal('ready').has_receivers_for(processor_a)
  True


Documenting Signals
-------------------

Both named and anonymous signals can be passed a ``doc`` argument at
construction to set the pydoc help text for the signal.  This
documentation will be picked up by most documentation generators (such
as sphinx) and is nice for documenting any additional data parameters
that will be sent down with the signal.


Async receivers
---------------

Receivers can be coroutine functions which can be called and awaited
via the :meth:`~Signal.send_async` method:

.. code-block:: python

   sig = blinker.Signal()

   async def receiver():
       ...

   sig.connect(receiver)
   await sig.send_async()

This however requires that all receivers are awaitable which then
precludes the usage of :meth:`~Signal.send`. To mix and match the
:meth:`~Signal.send_async` method takes a ``_sync_wrapper`` argument
such as:

.. code-block:: python

   sig = blinker.Signal()

   def receiver():
       ...

   sig.connect(receiver)

   def wrapper(func):

       async def inner(*args, **kwargs):
           func(*args, **kwargs)

       return inner

   await sig.send_async(_sync_wrapper=wrapper)

The equivalent usage for :meth:`~Signal.send` is via the
``_async_wrapper`` argument. This usage is will depend on your event
loop, and in the simple case whereby you aren't running within an
event loop the following example can be used:

.. code-block:: python

   sig = blinker.Signal()

   async def receiver():
       ...

   sig.connect(receiver)

   def wrapper(func):

       def inner(*args, **kwargs):
           asyncio.run(func(*args, **kwargs))

       return inner

   await sig.send(_async_wrapper=wrapper)


Call receivers in order of registration
---------------------------------------

It can be advantageous to call a signal's receivers in the order they
were registered. To achieve this the storage class for receivers should
be changed from an (unordered) set to an ordered set,

.. code-block:: python

    from blinker import Signal
    from ordered_set import OrderedSet

    Signal.set_class = OrderedSet

Please note that ``ordered_set`` is a PyPI package and is not
installed with blinker.


API Documentation
-----------------

All public API members can (and should) be imported from ``blinker``::

  from blinker import ANY, signal

Basic Signals
+++++++++++++

.. data:: ANY

    Symbol for "any sender".

.. autoclass:: Signal
   :members:

Named Signals
+++++++++++++

.. function:: signal(name, doc=None)

    Return a :class:`NamedSignal` in :data:`default_namespace` for the given
    name, creating it if required. Repeated calls with the same name return the
    same signal.

    :param name: The name of the signal.
    :type name: str
    :param doc: The docstring of the signal.
    :type doc: str | None
    :rtype: NamedSignal

.. data:: default_namespace

    A default :class:`Namespace` for creating named signals. :func:`signal`
    creates a :class:`NamedSignal` in this namespace.

.. autoclass:: NamedSignal
   :show-inheritance:

.. autoclass:: Namespace
   :show-inheritance:
   :members: signal


Changes
=======

.. include:: ../CHANGES.rst


MIT License
===========

.. literalinclude:: ../LICENSE.txt
    :language: text
