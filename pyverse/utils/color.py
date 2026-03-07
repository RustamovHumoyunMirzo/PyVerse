"""Color manipulation utilities."""
from __future__ import annotations
import colorsys
from typing import Tuple

RGB = Tuple[int, int, int]
RGBA = Tuple[int, int, int, float]


def hex_to_rgb(hex_color: str) -> RGB:
    h = hex_color.lstrip("#")
    if len(h) == 3:
        h = h[0]*2 + h[1]*2 + h[2]*2
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """(255, 87, 51) → '#ff5733'"""
    return f"#{r:02x}{g:02x}{b:02x}"


def lighten(hex_color: str, amount: float = 0.1) -> str:
    """Lighten a hex color by `amount` (0.0-1.0)."""
    r, g, b = hex_to_rgb(hex_color)
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    l = min(1.0, l + amount)
    r2, g2, b2 = colorsys.hls_to_rgb(h, l, s)
    return rgb_to_hex(int(r2*255), int(g2*255), int(b2*255))


def darken(hex_color: str, amount: float = 0.1) -> str:
    """Darken a hex color by `amount` (0.0-1.0)."""
    return lighten(hex_color, -amount)


def contrast_ratio(hex_a: str, hex_b: str) -> float:
    """WCAG contrast ratio between two hex colors (1.0-21.0)."""
    def relative_luminance(hex_c):
        rgb = [c / 255 for c in hex_to_rgb(hex_c)]
        lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]

    la, lb = relative_luminance(hex_a), relative_luminance(hex_b)
    lighter, darker = max(la, lb), min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def is_accessible(hex_fg: str, hex_bg: str, level: str = "AA") -> bool:
    """Check WCAG accessibility. level = 'AA' (4.5:1) or 'AAA' (7:1)."""
    ratio = contrast_ratio(hex_fg, hex_bg)
    return ratio >= (7.0 if level == "AAA" else 4.5)