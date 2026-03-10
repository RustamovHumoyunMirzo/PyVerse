# Core module

This module provides the foundational building blocks of a pyverse application — the app lifecycle, windowing, and the event system.

```python
from pyverse import core
```

---

## app

Application lifecycle and entry point.

---

**App**

```python
core.App()
```

Top-level application object. Owns an `EventEmitter` and exposes its full pub/sub API as first-class methods. Pass the instance to any subsystem that needs to emit or listen to events.

```python
app = core.App()
app.run()
```

---

**App.on**

```python
app.on(name: str, fn: Callable[..., Any], priority: int = 0) -> Callable[..., Any]
```

Register a persistent listener for an event. The listener remains active until removed with `off()`. Supports decorator usage.

```python
app.on("update", lambda dt: print(dt))

@app.on("ready")
def on_ready() -> None:
    print("Engine ready")
```

---

**App.once**

```python
app.once(name: str, fn: Callable[..., Any], priority: int = 0) -> Callable[..., Any]
```

Register a one-time listener. Automatically removed after its first invocation. Supports decorator usage.

```python
@app.once("init")
def bootstrap() -> None:
    load_assets()
```

---

**App.off**

```python
app.off(name: str, fn: Callable[..., Any]) -> None
```

Deregister a specific listener. No-op if the listener is not currently registered.

```python
app.off("resize", handle_resize)
```

---

**App.emit**

```python
app.emit(name: str, *args, **kwargs) -> Event | None
```

Emit a named event, invoking all registered listeners synchronously in descending priority order. Returns the `Event` created for the emission, or `None` if no listeners were registered.

```python
app.emit("collision", entity_a, entity_b, force=9.8)
```

---

**App.run**

```python
app.run() -> None
```

Start the pyverse engine and enter the main loop. **Blocks** until the engine exits. Register all listeners before calling `run()`.

Built-in lifecycle events fired by the engine:

| Event      | When                                      |
|------------|-------------------------------------------|
| `"ready"`  | Engine has initialised, before first tick |
| `"update"` | Each frame; receives `dt` (delta time)    |
| `"quit"`   | Application is about to exit              |

```python
app = core.App()

@app.on("update")
def tick(dt: float) -> None:
    simulate(dt)

app.run()
```

---

## window

OS window creation and configuration.

---

**Window**

```python
core.Window(width: int = 800, height: int = 600)
```

Create an application window with the given pixel dimensions. The window is not displayed until the owning `App` calls `run()` and the engine initialises the display context.

```python
# Default 800 × 600
win = core.Window()

# Custom resolution
win = core.Window(width=1920, height=1080)
```

| Argument | Type  | Default | Description                     |
|----------|-------|---------|---------------------------------|
| `width`  | `int` | `800`   | Horizontal size in pixels       |
| `height` | `int` | `600`   | Vertical size in pixels         |

---

## events

Pub/sub event system powering `App` and available for standalone use.

---

**EventEmitter**

```python
core.EventEmitter()
```

A standalone publish/subscribe emitter. Maintains a registry of named events, each with an ordered list of listener callbacks. Listeners are called synchronously in descending priority order.

```python
emitter = core.EventEmitter()
emitter.on("data", lambda payload: process(payload))
emitter.emit("data", payload={"key": "value"})
```

---

**EventEmitter.on**

```python
emitter.on(name: str, listener: Callable[..., Any], priority: int = 0) -> Callable[..., Any]
```

Register a persistent listener. Supports decorator usage.

```python
emitter.on("change", handle_change, priority=10)
```

---

**EventEmitter.once**

```python
emitter.once(name: str, listener: Callable[..., Any], priority: int = 0) -> Callable[..., Any]
```

Register a one-time listener. Removed automatically after first call. Supports decorator usage.

```python
emitter.once("connected", on_first_connect)
```

---

**EventEmitter.off**

```python
emitter.off(name: str, listener: Callable[..., Any]) -> None
```

Remove a specific listener by identity. No-op if not found.

```python
emitter.off("change", handle_change)
```

---

**EventEmitter.emit**

```python
emitter.emit(name: str, *args, **kwargs) -> Event | None
```

Invoke all listeners for *name*. One-time listeners are removed after invocation. Returns the `Event` object, or `None` if no listeners exist.

```python
emitter.emit("resize", width=1280, height=720)
```

---

**EventEmitter.clear**

```python
emitter.clear(name: str | None = None) -> None
```

Remove listeners from the registry. Pass a name to clear a single event; omit it to clear everything.

```python
emitter.clear("resize")   # remove only "resize" listeners
emitter.clear()           # remove all listeners for all events
```

---

**Event**

```python
core.Event(name: str, *args, **kwargs)
```

Represents a single occurrence of a named event. Created automatically by `EventEmitter.emit()` and returned to the call-site.

| Attribute  | Type    | Description                                           |
|------------|---------|-------------------------------------------------------|
| `name`     | `str`   | The event name (e.g. `"click"`)                       |
| `args`     | `tuple` | Positional arguments passed to `emit()`               |
| `kwargs`   | `dict`  | Keyword arguments passed to `emit()`                  |
| `stopped`  | `bool`  | `True` if propagation was halted via `stop()`         |

```python
event = emitter.emit("resize", width=1280, height=720)
print(event.name)     # "resize"
print(event.stopped)  # False
```

---

**Event.stop**

```python
event.stop() -> None
```

Halt propagation of this event. Sets `stopped = True`, causing the emitter to skip any remaining listeners in the current emission loop.

```python
def guard(value: int) -> None:
    if value < 0:
        event.stop()   # downstream listeners will not run

event = emitter.emit("validate", -1)
print(event.stopped)   # → True
```