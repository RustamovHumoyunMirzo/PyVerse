"""
Unit conversion helpers for desktop and mobile UI development.
All functions are pure — no side effects, no global state.
"""

_BASE_DP_DPI   = 160.0
_BASE_REM_PX   = 16.0


def pxToDp(px: float, dpi: float = _BASE_DP_DPI) -> float:
    """Convert physical pixels → density-independent pixels (dp/dip).

    Args:
        px:  Physical pixel value.
        dpi: Screen DPI (default 160 = mdpi baseline).

    Returns:
        dp value as float.

    Example:
        >>> utils.pxToDp(32, dpi=320)   # xxhdpi screen
        16.0
    """
    return px / (dpi / _BASE_DP_DPI)


def dpToPx(dp: float, dpi: float = _BASE_DP_DPI) -> float:
    """Convert dp → physical pixels.

    Example:
        >>> utils.dpToPx(16, dpi=320)
        32.0
    """
    return dp * (dpi / _BASE_DP_DPI)


def pxToSp(px: float, font_scale: float = 1.0, dpi: float = _BASE_DP_DPI) -> float:
    """Convert px → scale-independent pixels (sp) for font sizing.

    sp = dp / font_scale  (user's accessibility font scale factor)
    """
    return pxToDp(px, dpi) / font_scale


def remToPx(rem: float, base: float = _BASE_REM_PX) -> float:
    """Convert CSS rem → px.

    Example:
        >>> utils.remToPx(1.5)   # 24px at default 16px base
        24.0
    """
    return rem * base


def ptToPx(pt: float, dpi: float = 96.0) -> float:
    """Convert typographic points → pixels.
    1pt = 1/72 inch; at 96dpi → 1.333px
    """
    return pt * (dpi / 72.0)


def vwToPx(vw: float, viewport_width: float) -> float:
    """Convert CSS vw (viewport width %) → px."""
    return (vw / 100.0) * viewport_width


def vhToPx(vh: float, viewport_height: float) -> float:
    """Convert CSS vh (viewport height %) → px."""
    return (vh / 100.0) * viewport_height