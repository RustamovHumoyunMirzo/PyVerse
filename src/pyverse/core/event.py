class Event:

    def __init__(self, name, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        self.stopped = False

    def stop(self):
        self.stopped = True