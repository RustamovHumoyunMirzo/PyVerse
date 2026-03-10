from pyverse.pyverse import Window as _Window


class Window(_Window):

    def __init__(self, width=800, height=600):
        super().__init__(width, height)