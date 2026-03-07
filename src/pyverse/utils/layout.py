"""Layout math helpers."""


def clamp(value: float, min_val: float, max_val: float) -> float:
    """Clamp value between min and max. CSS clamp() equivalent."""
    return max(min_val, min(max_val, value))


def lerp(a: float, b: float, t: float) -> float:
    """Linear interpolate from a to b by t (0.0-1.0)."""
    return a + (b - a) * t


def remap(value: float, in_min: float, in_max: float,
          out_min: float, out_max: float) -> float:
    """Remap value from one range to another."""
    return out_min + (value - in_min) / (in_max - in_min) * (out_max - out_min)


def grid_columns(container_width: float, column_width: float,
                 gap: float = 16.0) -> int:
    """How many columns fit in a container?"""
    if container_width < column_width:
        return 1
    return max(1, int((container_width + gap) / (column_width + gap)))


_BREAKPOINTS = {
    "xs":  480,
    "sm":  640,
    "md":  768,
    "lg":  1024,
    "xl":  1280,
    "2xl": 1536,
}

def breakpoint(width: float) -> str:
    """Return the named breakpoint for a given pixel width.

    Example:
        >>> utils.breakpoint(800)
        'md'
    """
    result = "xs"
    for name, bp in _BREAKPOINTS.items():
        if width >= bp:
            result = name
    return result