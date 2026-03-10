from typing import Any, Callable, Optional

from pyverse.pyverse import _run_engine
from .events import EventEmitter
from .event import Event


class App:
    """
    Top-level application object.

    ``App`` is the central coordinator for a pyverse application. It owns an
    `EventEmitter` instance and exposes its full pub/sub API as
    first-class methods, so call-sites never need to interact with the emitter
    directly.

    Typical lifecycle::

        app = App()

        @app.on("ready")
        def on_ready() -> None:
            print("Engine is ready")

        app.run()   # blocks until the engine exits

    Attributes:
        events (EventEmitter): The underlying event emitter. Prefer the
            delegating helpers (`on`, `once`, `off`,
            `emit`) over accessing this attribute directly.
    """

    def __init__(self) -> None:
        """Initialise the application and its event emitter."""
        self.events: EventEmitter = EventEmitter()

    def on(
        self,
        name: str,
        fn: Optional[Callable[..., Any]] = None,
        priority: int = 0,
    ) -> Callable[..., Any]:
        """Register a persistent listener for *name*.

        Delegates to `EventEmitter.on`. The listener remains active
        until explicitly removed with `off`.

        Args:
            name: The event name to listen for.
            fn: Callable invoked each time the event fires.
            priority: Call-order priority; higher values run first.
                Defaults to ``0``.

        Returns:
        
            *fn* unchanged, enabling decorator usage::

                @app.on("update")
                def handle_update(dt: float) -> None:
                    ...
        """
        return self.events.on(name, fn, priority)

    def once(
        self,
        name: str,
        fn: Optional[Callable[..., Any]] = None,
        priority: int = 0,
    ) -> Callable[..., Any]:
        """Register a one-time listener for *name*.

        Delegates to `EventEmitter.once`. The listener is
        automatically removed after its first invocation.

        Args:
            name: The event name to listen for.
            fn: Callable invoked at most once when the event fires.
            priority: Call-order priority; higher values run first.
                Defaults to ``0``.

        Returns:

            *fn* unchanged, enabling decorator usage:

                @app.once("init")
                def bootstrap() -> None:
                    ...
        """
        return self.events.once(name, fn, priority)

    def off(self, name: str, fn: Callable[..., Any]) -> None:
        """Deregister a specific listener for *name*.

        Delegates to `EventEmitter.off`. No-op if *fn* is not
        currently registered for *name*.

        Args:
            name: The event name the listener was registered under.
            fn: The exact callable to remove.

        Example::

            app.off("resize", handle_resize)
        """
        self.events.off(name, fn)

    def emit(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Event]:
        """Emit *name*, invoking all registered listeners synchronously.

        Delegates to `EventEmitter.emit`. Listeners are called in
        descending priority order. One-time listeners are removed after
        invocation. Propagation stops early if any listener calls
        ``event.stop()``.

        Args:
            name: The event name to emit.
            *args: Positional arguments forwarded to every listener.
            **kwargs: Keyword arguments forwarded to every listener.

        Returns:
            The `Event` created for this emission, or ``None`` if
            no listeners were registered for *name*.

        Example::

            app.emit("collision", entity_a, entity_b, force=9.8)
        """
        return self.events.emit(name, *args, **kwargs)

    def run(self) -> None:
        """Start the pyverse engine and enter the main loop.

        Passes this ``App`` instance to the internal ``_run_engine``
        function, which takes ownership of the execution loop. This call
        **blocks** until the engine exits (e.g. the window is closed or
        the application is terminated programmatically).

        The engine will fire built-in lifecycle events (such as ``"ready"``,
        ``"update"``, ``"quit"``) on this app instance during its run.
        Register listeners before calling `run` to handle them.

        Example::

            app = App()
            app.on("quit", lambda: print("Goodbye"))
            app.run()
        """
        _run_engine(self)