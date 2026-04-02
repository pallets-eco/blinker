# Blinker

Blinker provides a fast dispatching system that allows any number of
interested parties to subscribe to events, or "signals".


## Pallets Community Ecosystem

> [!IMPORTANT]\
> This project is part of the Pallets Community Ecosystem. Pallets is the open
> source organization that maintains Flask; Pallets-Eco enables community
> maintenance of related projects. If you are interested in helping maintain
> this project, please reach out on [the Pallets Discord server][discord].
>
> [discord]: https://discord.gg/pallets


## Example

Signal receivers can subscribe to specific senders or receive signals
sent by any sender.

```pycon
>>> from blinker import signal
>>> started = signal('round-started')
>>> def each(round):
...     print(f"Round {round}")
...
>>> started.connect(each)

>>> def round_two(round):
...     print("This is round two.")
...
>>> started.connect(round_two, sender=2)

>>> for round in range(1, 4):
...     started.send(round)
...
Round 1!
Round 2!
This is round two.
Round 3!
```

## Contributing
Blinker uses [uv](https://docs.astral.sh/uv/) to manage its dependencies and developer environment. With the repository checked out, to install version of Python that Bilnker supports, create your virtual environment, and install the required dependencies, run:

```bash
uv sync
```

This will install Blinker including development dependencies, such as those related to auto style, pre-commit etc.

Tests are run with [pytest](https://docs.pytest.org/en/stable/). To just run the test suite with the default python installation, use:

```bash
uv run pytest
```

To run the test suite against any supported python versions, and also run other checks performed by CI, use:

```bash
# run against python 3.13
uv run tox -e py13

# or run against all supported versions
uv run tox
```

This will create `.tox` directory taht contains a separate folder for each supported python version, thus you can activate any of them. For example to test the Blinker under python 3.11, run:

```bash
./.tox/py3.11/Scripts/activate
```