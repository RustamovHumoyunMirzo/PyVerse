from pyverse.pyverse import Window as _Window


class Window(_Window):
    """
    An application window with sensible default dimensions.

    Thin subclass of the internal `pyverse.pyverse.Window` that
    pre-fills ``width`` and ``height`` so call-sites don't need to repeat
    the common 800 × 600 default. All other behaviour — rendering, event
    dispatch, OS integration — is inherited unchanged from the base class.

    Args:
        width (int): Width of the window in pixels. Defaults to ``800``.
        height (int): Height of the window in pixels. Defaults to ``600``.

    Example::

        # Default 800 × 600 window
        win = Window()

        # Custom resolution
        win = Window(width=1920, height=1080)

    .. note::
        The window is not displayed until the owning `App` calls
        `App.run` and the engine initialises the display context.
    """

    def __init__(self, width: int = 800, height: int = 600) -> None:
        """
        Args:
            width: Horizontal size of the window in pixels. Defaults to ``800``.
            height: Vertical size of the window in pixels. Defaults to ``600``.
        """
        super().__init__(width, height)