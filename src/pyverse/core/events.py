from typing import Any, Callable, Optional
from .event import Event


class EventEmitter:
    """
    A simple publish/subscribe event emitter.

    Maintains a registry of named events, each with an ordered list of
    listener callbacks. Listeners are called synchronously in descending
    priority order when an event is emitted.

    Attributes:
        _events (dict[str, list[dict]]): Internal mapping of event names to
            their registered listener descriptors. Each descriptor is a dict
            with the keys ``fn``, ``priority``, and ``once``.

    Example::

        emitter = EventEmitter()

        def on_login(user_id: int) -> None:
            print(f"User {user_id} logged in")

        emitter.on("login", on_login)
        emitter.emit("login", user_id=42)
    """

    def __init__(self) -> None:
        """Initialise the emitter with an empty event registry."""
        self._events: dict[str, list[dict]] = {}

    def on(
        self,
        name: str,
        listener: Optional[Callable[..., Any]] = None,
        priority: int = 0,
    ) -> Callable[..., Any]:
        """Register a persistent listener for *name*.

        The listener remains registered until explicitly removed with
        `off` or the event is cleared with `clear`.

        Args:
            name: The event name to listen for (e.g. ``"click"``).
            listener: A callable invoked with the event's positional and
                keyword arguments when the event fires.
            priority: Determines the call order among listeners for the
                same event. Higher values are called first. Listeners
                with equal priority are called in registration order.
                Defaults to ``0``.

        Returns:
            The *listener* callable, unchanged. Returned so the method
            can be used as a decorator::

                @emitter.on("ready")
                def handle_ready() -> None:
                    ...

        Example::

            emitter.on("data", lambda payload: process(payload), priority=10)
        """
        def register(fn: Callable[..., Any]) -> Callable[..., Any]:
            listeners = self._events.setdefault(name, [])

            listeners.append({
                "fn": fn,
                "priority": priority,
                "once": False,
            })

            listeners.sort(key=lambda x: x["priority"], reverse=True)
            return fn

        if listener is None:
            return register

        return register(listener)

    def once(
        self,
        name: str,
        listener: Optional[Callable[..., Any]] = None,
        priority: int = 0,
    ) -> Callable[..., Any]:
        """Register a one-time listener for *name*.

        Identical to `on`, except the listener is automatically
        removed after it is invoked for the first time.

        Args:
            name: The event name to listen for.
            listener: A callable invoked at most once when the event fires.
            priority: Call-order priority (higher = earlier). Defaults to ``0``.

        Returns:
            The *listener* callable, unchanged. Supports decorator usage
            identically to `on`.

        Example::

            @emitter.once("init")
            def bootstrap() -> None:
                # Called only on the very first "init" emission.
                ...
        """
        def register(fn: Callable[..., Any]) -> Callable[..., Any]:
            listeners = self._events.setdefault(name, [])

            listeners.append({
                "fn": fn,
                "priority": priority,
                "once": True,
            })

            listeners.sort(key=lambda x: x["priority"], reverse=True)
            return fn

        if listener is None:
            return register

        return register(listener)

    def off(self, name: str, listener: Callable[..., Any]) -> None:
        """Deregister a specific listener for *name*.

        Removes all descriptors whose ``fn`` matches *listener* by
        identity. If *name* has no registered listeners, or *listener*
        is not found, the call is a no-op.

        Args:
            name: The event name the listener was registered under.
            listener: The exact callable that was passed to `on`
                or `once`.

        Example::

            def handler(value: int) -> None:
                ...

            emitter.on("change", handler)
            emitter.off("change", handler)  # handler will no longer be called
        """
        listeners = self._events.get(name)

        if not listeners:
            return

        self._events[name] = [l for l in listeners if l["fn"] != listener]

    def emit(
        self,
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> Optional[Event]:
        """Emit an event, invoking all listeners registered under *name*.

        Listeners are called synchronously in descending priority order,
        receiving the positional and keyword arguments stored on the
        :class:`Event` object (i.e. whatever was passed as *args* /
        *kwargs* here).

        One-time listeners (registered via `once`) are removed
        immediately after they are called.

        Propagation can be halted mid-loop: if any listener calls
        ``event.stop()`` (setting ``event.stopped = True``), no
        subsequent listeners are invoked for that emission.

        Args:
            name: The event name to emit.
            *args: Positional arguments forwarded to every listener.
            **kwargs: Keyword arguments forwarded to every listener.

        Returns:
            The :class:`Event` instance created for this emission, which
            carries the original *args* / *kwargs* and any state set by
            listeners (e.g. ``stopped``). Returns ``None`` if no
            listeners are registered for *name*.

        Example::

            event = emitter.emit("message", "hello", user_id=7)
            if event and event.stopped:
                print("Propagation was stopped by a listener")
        """
        listeners = self._events.get(name)

        if not listeners:
            return None

        event = Event(name, *args, **kwargs)

        for item in list(listeners):
            item["fn"](*event.args, **event.kwargs)

            if item["once"]:
                self.off(name, item["fn"])

            if event.stopped:
                break

        return event

    def clear(self, name: Optional[str] = None) -> None:
        """Remove listeners from the registry.

        Args:
            name: When provided, only listeners for this event name are
                removed. When omitted (or ``None``), **all** events and
                their listeners are cleared.

        Example::

            emitter.clear("resize")   # remove only "resize" listeners
            emitter.clear()           # remove every registered listener
        """
        if name is None:
            self._events.clear()
        else:
            self._events.pop(name, None)