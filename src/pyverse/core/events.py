from .event import Event


class EventEmitter:

    def __init__(self):
        self._events = {}

    def on(self, name, listener, priority=0):
        listeners = self._events.setdefault(name, [])

        listeners.append({
            "fn": listener,
            "priority": priority,
            "once": False
        })

        listeners.sort(key=lambda x: x["priority"], reverse=True)

        return listener

    def once(self, name, listener, priority=0):
        listeners = self._events.setdefault(name, [])

        listeners.append({
            "fn": listener,
            "priority": priority,
            "once": True
        })

        listeners.sort(key=lambda x: x["priority"], reverse=True)

        return listener

    def off(self, name, listener):
        listeners = self._events.get(name)

        if not listeners:
            return

        self._events[name] = [
            l for l in listeners if l["fn"] != listener
        ]

    def emit(self, name, *args, **kwargs):
        listeners = self._events.get(name)

        if not listeners:
            return

        event = Event(name, *args, **kwargs)

        for item in list(listeners):

            item["fn"](*event.args, **event.kwargs)

            if item["once"]:
                self.off(name, item["fn"])

            if event.stopped:
                break

        return event

    def clear(self, name=None):
        if name is None:
            self._events.clear()
        else:
            self._events.pop(name, None)