Version 1.5
-----------

Released 2022-07-17

-   Support Python >= 3.7 and PyPy. Python 2, Python < 3.7, and Jython
    may continue to work, but the next release will make incompatible
    changes.


Version 1.4
-----------

Released 2015-07-23

-   Verified Python 3.4 support, no changes needed.
-   Additional bookkeeping cleanup for non-``ANY`` connections at
    disconnect time.
-   Added ``Signal._cleanup_bookeeping()`` to prune stale bookkeeping on
    demand.


Version 1.3
-----------

Released 2013-07-03

-   The global signal stash behind ``signal()`` is now backed by a
    regular name-to-``Signal`` dictionary. Previously, weak references
    were held in the mapping and ephermal usage in code like
    ``signal('foo').connect(...)`` could have surprising program
    behavior depending on import order of modules.
-   ``Namespace`` is now built on a regular dict. Use ``WeakNamespace``
    for the older, weak-referencing behavior.
-   ``Signal.connect('text-sender')`` uses an alterate hashing strategy
    to avoid sharp edges in text identity.


Version 1.2
-----------

Released 2011-10-26

-   Added ``Signal.receiver_connected`` and
    ``Signal.receiver_disconnected`` per-``Signal`` signals.
-   Deprecated the global ``receiver_connected`` signal.
-   Verified Python 3.2 support, no changes needed.


Version 1.1
-----------

Released 2010-07-21

-   Added ``@signal.connect_via(sender)`` decorator
-   Added ``signal.connected_to`` shorthand name for the
    ``temporarily_connected_to`` context manager.


Version 1.0
-----------

Released 2010-03-28

-   Python 3.0 and 3.1 compatibility.


Version 0.9
-----------

Released 2010-02-26

-   Added ``Signal.temporarily_connected_to`` context manager.
-   Docs! Sphinx docs, project web site.


Version 0.8
-----------

Released 2010-02-14

-   Initial release.
-   Extracted from ``flatland.util.signals``.
-   Added Python 2.4 compatibility.
-   Added nearly functional Python 3.1 compatibility. Everything except
    connecting to instance methods seems to work.
