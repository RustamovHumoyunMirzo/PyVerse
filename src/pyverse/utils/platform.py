"""Screen / platform detection helpers."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SafeAreaInsets:
    top: float = 0.0
    right: float = 0.0
    bottom: float = 0.0
    left: float = 0.0


def screen_dpi() -> float:
    """Best-effort screen DPI via platform APIs."""
    try:
        import ctypes
        dc = ctypes.windll.user32.GetDC(0)
        dpi = ctypes.windll.gdi32.GetDeviceCaps(dc, 88)
        ctypes.windll.user32.ReleaseDC(0, dc)
        return float(dpi)
    except Exception:
        pass
    try:
        import subprocess
        out = subprocess.check_output(["xdpyinfo"], text=True)
        for line in out.splitlines():
            if "dots per inch" in line:
                return float(line.split()[1])
    except Exception:
        pass
    return 96.0


def is_mobile_density(dpi: float | None = None) -> bool:
    """True if DPI suggests a mobile/HiDPI screen (≥ 240)."""
    return (dpi or screen_dpi()) >= 240.0


def logical_resolution(physical_w: float, physical_h: float,
                        dpi: float | None = None) -> tuple[float, float]:
    """Convert physical resolution → logical (dp) resolution."""
    d = dpi or screen_dpi()
    scale = d / 160.0
    return physical_w / scale, physical_h / scale


def safe_area_insets(platform: str = "auto") -> SafeAreaInsets:
    """
    Return safe area insets for the target platform.
    'auto' detects OS; or pass 'ios', 'android', 'desktop'.
    """
    import sys
    p = platform.lower()
    if p == "auto":
        p = "ios" if sys.platform == "darwin" else \
            "android" if "android" in sys.platform else "desktop"

    if p == "ios":
        return SafeAreaInsets(top=44.0, right=0.0, bottom=34.0, left=0.0)
    elif p == "android":
        return SafeAreaInsets(top=24.0, right=0.0, bottom=16.0, left=0.0)
    return SafeAreaInsets()