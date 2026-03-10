from pyverse.pyverse import _run_engine
from .events import EventEmitter


class App:

    def __init__(self):
        self.events = EventEmitter()

    def on(self, name, fn, priority=0):
        return self.events.on(name, fn, priority)

    def once(self, name, fn, priority=0):
        return self.events.once(name, fn, priority)

    def off(self, name, fn):
        self.events.off(name, fn)

    def emit(self, name, *args, **kwargs):
        return self.events.emit(name, *args, **kwargs)

    def run(self):
        _run_engine(self)