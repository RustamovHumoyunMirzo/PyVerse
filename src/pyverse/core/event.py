from typing import Any


class Event:
    """
    Represents a single occurrence of a named event.

    Created automatically by `EventEmitter.emit` and passed — via its
    ``args`` / ``kwargs`` attributes — to every registered listener.
    Listeners may inspect or mutate the event (e.g. call `stop`) but
    do not receive the ``Event`` object itself; they receive the unpacked
    positional and keyword arguments.

    Attributes:
        name (str): The name of the event (e.g. ``"click"`` or ``"resize"``).
        args (tuple[Any, ...]): Positional arguments supplied to
            `EventEmitter.emit`, forwarded to each listener.
        kwargs (dict[str, Any]): Keyword arguments supplied to
            `EventEmitter.emit`, forwarded to each listener.
        stopped (bool): When ``True``, the emitter stops invoking further
            listeners for this emission. Set via `stop`.
            Defaults to ``False``.

    Example::

        # EventEmitter creates and returns this automatically:
        event = emitter.emit("resize", width=1280, height=720)
        print(event.name)     # "resize"
        print(event.stopped)  # False (unless a listener called event.stop())
    """

    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
        """
        Args:
            name: The event name identifier.
            *args: Positional arguments to forward to listeners.
            **kwargs: Keyword arguments to forward to listeners.
        """
        self.name: str = name
        self.args: tuple[Any, ...] = args
        self.kwargs: dict[str, Any] = kwargs
        self.stopped: bool = False

    def stop(self) -> None:
        """Halt propagation of this event.

        Sets :attr:`stopped` to ``True``, signalling the emitter to skip
        any remaining listeners in the current emission loop. Has no effect
        if called outside of an active emission (e.g. after
        `EventEmitter.emit` has already returned).

        Example::

            def guard_listener(value: int) -> None:
                if value < 0:
                    event.stop()   # prevent downstream listeners from running

        .. note::
            ``event`` must be captured from the emitter's return value, or
            accessed via a closure, since listeners receive unpacked args —
            not the ``Event`` object directly.
        """
        self.stopped = True