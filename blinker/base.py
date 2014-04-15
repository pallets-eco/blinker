# -*- coding: utf-8; fill-column: 76 -*-
"""Signals and events.

A small implementation of signals, inspired by a snippet of Django signal
API client code seen in a blog post.  Signals are first-class objects and
each manages its own receivers and message emission.

The :func:`signal` function provides singleton behavior for named signals.

"""
from warnings import warn
from weakref import WeakValueDictionary

from blinker._utilities import (
    WeakTypes,
    contextmanager,
    defaultdict,
    hashable_identity,
    lazy_property,
    reference,
    symbol,
    )


ANY = symbol('ANY')
ANY.__doc__ = 'Token for "any sender".'
ANY_ID = 0


class Signal(object):
    """A notification emitter."""

    #: An :obj:`ANY` convenience synonym, allows ``Signal.ANY``
    #: without an additional import.
    ANY = ANY

    @lazy_property
    def receiver_connected(self):
        """Emitted after each :meth:`connect`.

        The signal sender is the signal instance, and the :meth:`connect`
        arguments are passed through: *receiver*, *sender*, and *weak*.

        .. versionadded:: 1.2

        """
        return Signal(doc="Emitted after a receiver connects.")

    @lazy_property
    def receiver_disconnected(self):
        """Emitted after :meth:`disconnect`.

        The sender is the signal instance, and the :meth:`disconnect` arguments
        are passed through: *receiver* and *sender*.

        Note, this signal is emitted **only** when :meth:`disconnect` is
        called explicitly.

        The disconnect signal can not be emitted by an automatic disconnect
        (due to a weakly referenced receiver or sender going out of scope),
        as the receiver and/or sender instances are no longer available for
        use at the time this signal would be emitted.

        An alternative approach is available by subscribing to
        :attr:`receiver_connected` and setting up a custom weakref cleanup
        callback on weak receivers and senders.

        .. versionadded:: 1.2

        """
        return Signal(doc="Emitted after a receiver disconnects.")

    def __init__(self, doc=None):
        """
        :param doc: optional.  If provided, will be assigned to the signal's
          __doc__ attribute.

        """
        if doc:
            self.__doc__ = doc
        #: A mapping of connected receivers.
        #:
        #: The values of this mapping are not meaningful outside of the
        #: internal :class:`Signal` implementation, however the boolean value
        #: of the mapping is useful as an extremely efficient check to see if
        #: any receivers are connected to the signal.
        self.receivers = {}
        self._by_receiver = defaultdict(set)
        self._by_sender = defaultdict(set)
        self._weak_senders = {}

    def connect(self, receiver, sender=ANY, weak=True):
        """Connect *receiver* to signal events sent by *sender*.

        :param receiver: A callable.  Will be invoked by :meth:`send` with
          `sender=` as a single positional argument and any \*\*kwargs that
          were provided to a call to :meth:`send`.

        :param sender: Any object or :obj:`ANY`, defaults to ``ANY``.
          Restricts notifications delivered to *receiver* to only those
          :meth:`send` emissions sent by *sender*.  If ``ANY``, the receiver
          will always be notified.  A *receiver* may be connected to
          multiple *sender* values on the same Signal through multiple calls
          to :meth:`connect`.

        :param weak: If true, the Signal will hold a weakref to *receiver*
          and automatically disconnect when *receiver* goes out of scope or
          is garbage collected.  Defaults to True.

        """
        receiver_id = hashable_identity(receiver)
        if weak:
            receiver_ref = reference(receiver, self._cleanup_receiver)
            receiver_ref.receiver_id = receiver_id
        else:
            receiver_ref = receiver
        if sender is ANY:
            sender_id = ANY_ID
        else:
            sender_id = hashable_identity(sender)

        self.receivers.setdefault(receiver_id, receiver_ref)
        self._by_sender[sender_id].add(receiver_id)
        self._by_receiver[receiver_id].add(sender_id)
        del receiver_ref

        if sender is not ANY and sender_id not in self._weak_senders:
            # wire together a cleanup for weakref-able senders
            try:
                sender_ref = reference(sender, self._cleanup_sender)
                sender_ref.sender_id = sender_id
            except TypeError:
                pass
            else:
                self._weak_senders.setdefault(sender_id, sender_ref)
                del sender_ref

        # broadcast this connection.  if receivers raise, disconnect.
        try:
            self.receiver_connected.send(sentby=self,
                                         receiver=receiver,
                                         sender=sender,
                                         weak=weak)
        except:
            self.disconnect(receiver, sender)
            raise
        return receiver

    def connect_via(self, sender, weak=False):
        """Connect the decorated function as a receiver for *sender*.

        :param sender: Any object or :obj:`ANY`.  The decorated function
          will only receive :meth:`send` emissions sent by *sender*.  If
          ``ANY``, the receiver will always be notified.  A function may be
          decorated multiple times with differing *sender* values.

        :param weak: If true, the Signal will hold a weakref to the
          decorated function and automatically disconnect when *receiver*
          goes out of scope or is garbage collected.  Unlike
          :meth:`connect`, this defaults to False.

        The decorated function will be invoked by :meth:`send` with
          `sender=` as a single positional argument and any \*\*kwargs that
          were provided to the call to :meth:`send`.


        .. versionadded:: 1.1

        """
        def decorator(fn):
            self.connect(fn, sender, weak)
            return fn
        return decorator

    @contextmanager
    def connected_to(self, receiver, sender=ANY):
        """Execute a block with the signal temporarily connected to *receiver*.

        :param receiver: a receiver callable
        :param sender: optional, a sender to filter on

        This is a context manager for use in the ``with`` statement.  It can
        be useful in unit tests.  *receiver* is connected to the signal for
        the duration of the ``with`` block, and will be disconnected
        automatically when exiting the block:

        .. testsetup::

          from __future__ import with_statement
          from blinker import Signal
          on_ready = Signal()
          receiver = lambda sender: None

        .. testcode::

          with on_ready.connected_to(receiver):
             # do stuff
             on_ready.send(123)

        .. versionadded:: 1.1

        """
        self.connect(receiver, sender=sender, weak=False)
        try:
            yield None
        except:
            self.disconnect(receiver)
            raise
        else:
            self.disconnect(receiver)

    def temporarily_connected_to(self, receiver, sender=ANY):
        """An alias for :meth:`connected_to`.

        :param receiver: a receiver callable
        :param sender: optional, a sender to filter on

        .. versionadded:: 0.9

        .. versionchanged:: 1.1
          Renamed to :meth:`connected_to`.  ``temporarily_connected_to``
          was deprecated in 1.2 and removed in a subsequent version.

        """
        warn("temporarily_connected_to is deprecated; "
             "use connected_to instead.",
             DeprecationWarning)
        return self.connected_to(receiver, sender)

    def send(self, sender=None, *args, sentby=None, **kwargs):
        """Emit this signal on behalf of *sender*, passing on \*\*kwargs.

        Returns a list of 2-tuples, pairing receivers with their return
        value. The ordering of receiver notification is undefined.

        :param sender: Any object or ``None``.
        
        :param sentby: Only used by the implementation.  This should not be 
          given directly by the user; it is present so 
          :attr:`receiver_connected` can differentiate between the message to 
          be sent (`sender`) and the signal which sent it (`sentby`) to ensure
          that the correct receivers are called with the correct arguments.  
          Basically, *you should never call this method with this argument 
          unless you are absolutely certain that you should.*
        
        :param \*args: Positional arguments to be sent to receivers.
        
        :param \*\*kwargs: Keyword arguments to be sent to receivers.

        """

        if not self.receivers:
            return []
        else:
            if not sentby:
                return [(receiver, receiver(sender, *args, **kwargs))
                        for receiver in self.receivers_for(sender)]
            else:
                kwargs['sender'] = sender
                return [(receiver, receiver(sentby, *args, **kwargs))
                        for receiver in self.receivers_for(sentby)]
    def has_receivers_for(self, sender):
        """True if there is probably a receiver for *sender*.

        Performs an optimistic check only.  Does not guarantee that all
        weakly referenced receivers are still alive.  See
        :meth:`receivers_for` for a stronger search.

        """
        if not self.receivers:
            return False
        if self._by_sender[ANY_ID]:
            return True
        if sender is ANY:
            return False
        return hashable_identity(sender) in self._by_sender

    def receivers_for(self, sender):
        """Iterate all live receivers listening for *sender*."""
        # TODO: test receivers_for(ANY)
        if self.receivers:
            sender_id = hashable_identity(sender)
            if sender_id in self._by_sender:
                ids = (self._by_sender[ANY_ID] |
                       self._by_sender[sender_id])
            else:
                ids = self._by_sender[ANY_ID].copy()
            for receiver_id in ids:
                receiver = self.receivers.get(receiver_id)
                if receiver is None:
                    continue
                if isinstance(receiver, WeakTypes):
                    strong = receiver()
                    if strong is None:
                        self._disconnect(receiver_id, ANY_ID)
                        continue
                    receiver = strong
                yield receiver

    def disconnect(self, receiver, sender=ANY):
        """Disconnect *receiver* from this signal's events.

        :param receiver: a previously :meth:`connected<connect>` callable

        :param sender: a specific sender to disconnect from, or :obj:`ANY`
          to disconnect from all senders.  Defaults to ``ANY``.

        """
        if sender is ANY:
            sender_id = ANY_ID
        else:
            sender_id = hashable_identity(sender)
        receiver_id = hashable_identity(receiver)
        self._disconnect(receiver_id, sender_id)

        self.receiver_disconnected.send(sentby=self,
                                        receiver=receiver,
                                        sender=sender)

    def _disconnect(self, receiver_id, sender_id):
        if sender_id == ANY_ID:
            if self._by_receiver.pop(receiver_id, False):
                for bucket in self._by_sender.values():
                    bucket.discard(receiver_id)
            self.receivers.pop(receiver_id, None)
        else:
            self._by_sender[sender_id].discard(receiver_id)

    def _cleanup_receiver(self, receiver_ref):
        """Disconnect a receiver from all senders."""
        self._disconnect(receiver_ref.receiver_id, ANY_ID)

    def _cleanup_sender(self, sender_ref):
        """Disconnect all receivers from a sender."""
        sender_id = sender_ref.sender_id
        assert sender_id != ANY_ID
        self._weak_senders.pop(sender_id, None)
        for receiver_id in self._by_sender.pop(sender_id, ()):
            self._by_receiver[receiver_id].discard(sender_id)

    def _clear_state(self):
        """Throw away all signal state.  Useful for unit tests."""
        self._weak_senders.clear()
        self.receivers.clear()
        self._by_sender.clear()
        self._by_receiver.clear()


class NamedSignal(Signal):
    """A named generic notification emitter."""

    def __init__(self, name, doc=None):
        Signal.__init__(self, doc)

        #: The name of this signal.
        self.name = name

    def __repr__(self):
        base = Signal.__repr__(self)
        return "%s; %r>" % (base[:-1], self.name)


class Namespace(dict):
    """A mapping of signal names to signals."""

    def signal(self, name, doc=None):
        """Return the :class:`NamedSignal` *name*, creating it if required.

        Repeated calls to this function will return the same signal object.

        """
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))


class WeakNamespace(WeakValueDictionary):
    """A weak mapping of signal names to signals.

    Automatically cleans up unused Signals when the last reference goes out
    of scope.  This namespace implementation exists for a measure of legacy
    compatibility with Blinker <= 1.2, and may be dropped in the future.

    """

    def signal(self, name, doc=None):
        """Return the :class:`NamedSignal` *name*, creating it if required.

        Repeated calls to this function will return the same signal object.

        """
        try:
            return self[name]
        except KeyError:
            return self.setdefault(name, NamedSignal(name, doc))


signal = Namespace().signal
