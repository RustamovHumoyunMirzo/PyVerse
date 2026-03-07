# Utils module

This module is considered a utility and helps you with units, colors, layout math, and platform detection.

```python
from pyverse import utils
```

---

## units

Pixel and unit conversion helpers for desktop and mobile UI development.

---

**pxToDp**

```python
utils.pxToDp(px: float, dpi: float = 160.0) -> float
```

Convert physical pixels to density-independent pixels (dp). Uses Android's mdpi baseline of 160 DPI.

```python
utils.pxToDp(32, dpi=320)   # → 16.0
utils.pxToDp(16, dpi=160)   # → 16.0
```

---

**dpToPx**

```python
utils.dpToPx(dp: float, dpi: float = 160.0) -> float
```

Convert density-independent pixels back to physical pixels.

```python
utils.dpToPx(16, dpi=320)   # → 32.0
```

---

**pxToSp**

```python
utils.pxToSp(px: float, font_scale: float = 1.0, dpi: float = 160.0) -> float
```

Convert px to scale-independent pixels (sp), used for font sizing. Accounts for the user's system font scale factor.

```python
utils.pxToSp(32, font_scale=1.5, dpi=320)   # → 10.67
```

---

**remToPx**

```python
utils.remToPx(rem: float, base: float = 16.0) -> float
```

Convert CSS `rem` units to pixels. Defaults to the browser standard of 16px base.

```python
utils.remToPx(1.5)            # → 24.0
utils.remToPx(2.0, base=20)   # → 40.0
```

---

**ptToPx**

```python
utils.ptToPx(pt: float, dpi: float = 96.0) -> float
```

Convert typographic points to pixels. 1pt = 1/72 inch; at 96 DPI → 1.333px.

```python
utils.ptToPx(12)   # → 16.0
```

---

**vwToPx**

```python
utils.vwToPx(vw: float, viewport_width: float) -> float
```

Convert CSS `vw` (viewport width percentage) to pixels.

```python
utils.vwToPx(50, 1920)   # → 960.0
```

---

**vhToPx**

```python
utils.vhToPx(vh: float, viewport_height: float) -> float
```

Convert CSS `vh` (viewport height percentage) to pixels.

```python
utils.vhToPx(25, 1080)   # → 270.0
```

---

## color

Color parsing, manipulation, and WCAG accessibility helpers.

---

**hex_to_rgb**

```python
utils.hex_to_rgb(hex_color: str) -> tuple[int, int, int]
```

Parse a hex color string to an `(R, G, B)` tuple. Supports both 3-digit (`#fff`) and 6-digit (`#ffffff`) shorthand.

```python
utils.hex_to_rgb("#FF5733")   # → (255, 87, 51)
utils.hex_to_rgb("#fff")      # → (255, 255, 255)
```

---

**rgb_to_hex**

```python
utils.rgb_to_hex(r: int, g: int, b: int) -> str
```

Convert R, G, B integer values to a lowercase hex color string.

```python
utils.rgb_to_hex(255, 87, 51)   # → "#ff5733"
```

---

**lighten**

```python
utils.lighten(hex_color: str, amount: float = 0.1) -> str
```

Lighten a color by `amount` (0.0–1.0) in HLS color space.

```python
utils.lighten("#FF5733", 0.2)   # → "#ffab99"
```

---

**darken**

```python
utils.darken(hex_color: str, amount: float = 0.1) -> str
```

Darken a color by `amount` (0.0–1.0) in HLS color space. Inverse of `lighten`.

```python
utils.darken("#FF5733", 0.15)   # → darker shade
```

---

**contrast_ratio**

```python
utils.contrast_ratio(hex_a: str, hex_b: str) -> float
```

Calculate the WCAG relative contrast ratio between two colors. Returns a value from `1.0` (no contrast) to `21.0` (black on white).

```python
utils.contrast_ratio("#ffffff", "#000000")   # → 21.0
utils.contrast_ratio("#767676", "#ffffff")   # → 4.54
```

---

**is_accessible**

```python
utils.is_accessible(hex_fg: str, hex_bg: str, level: str = "AA") -> bool
```

Check whether a foreground/background pair meets WCAG standards.

| Level | Minimum ratio | Use case            |
|-------|---------------|---------------------|
| `AA`  | 4.5 : 1       | Normal text         |
| `AAA` | 7.0 : 1       | Enhanced / small text |

```python
utils.is_accessible("#767676", "#fff")          # → True
utils.is_accessible("#767676", "#fff", "AAA")   # → False
```

---

## layout

Responsive layout math and grid helpers.

---

**clamp**

```python
utils.clamp(value: float, min_val: float, max_val: float) -> float
```

Constrain a value between a minimum and maximum. Equivalent to CSS `clamp()`.

```python
utils.clamp(150, 0, 100)   # → 100
utils.clamp(-5,  0, 100)   # → 0
utils.clamp(50,  0, 100)   # → 50
```

---

**lerp**

```python
utils.lerp(a: float, b: float, t: float) -> float
```

Linear interpolation from `a` to `b` by factor `t` (0.0–1.0). Useful for animations and smooth transitions.

```python
utils.lerp(0, 100, 0.25)   # → 25.0
utils.lerp(0, 100, 0.5)    # → 50.0
```

---

**remap**

```python
utils.remap(value, in_min, in_max, out_min, out_max) -> float
```

Remap a value from one numeric range to another.

```python
# Map a 0–255 sensor value to a 0–100 percentage
utils.remap(128, 0, 255, 0, 100)   # → 50.2
```

---

**grid_columns**

```python
utils.grid_columns(container_width: float, column_width: float, gap: float = 16.0) -> int
```

Calculate how many fixed-width columns fit inside a container, accounting for gaps.

```python
utils.grid_columns(1200, 300, gap=16)   # → 3
utils.grid_columns(768,  300, gap=16)   # → 2
```

---

**breakpoint**

```python
utils.breakpoint(width: float) -> str
```

Return the named responsive breakpoint for a given pixel width, matching Tailwind CSS conventions.

| Name  | Min width | Typical device              |
|-------|-----------|-----------------------------|
| `xs`  | 480px     | Small mobile                |
| `sm`  | 640px     | Mobile landscape            |
| `md`  | 768px     | Tablet portrait             |
| `lg`  | 1024px    | Tablet landscape / desktop  |
| `xl`  | 1280px    | Desktop                     |
| `2xl` | 1536px    | Wide desktop                |

```python
utils.breakpoint(500)    # → "sm"
utils.breakpoint(900)    # → "lg"
utils.breakpoint(1600)   # → "2xl"
```

---

## platform

Screen DPI, safe area insets, and platform detection helpers.

---

**screen_dpi**

```python
utils.screen_dpi() -> float
```

Detect the current screen's DPI using native platform APIs. Falls back to `96.0` if detection fails. Supports Windows (GDI), Linux (xdpyinfo), and macOS.

```python
dpi = utils.screen_dpi()   # → 96.0, 144.0, 192.0, etc.
```

---

**is_mobile_density**

```python
utils.is_mobile_density(dpi: float | None = None) -> bool
```

Return `True` if the screen DPI is 240 or higher, which typically indicates a mobile or HiDPI display. Calls `screen_dpi()` automatically if no value is passed.

```python
utils.is_mobile_density(96)    # → False
utils.is_mobile_density(320)   # → True
```

---

**logical_resolution**

```python
utils.logical_resolution(physical_w: float, physical_h: float, dpi: float | None = None) -> tuple[float, float]
```

Convert a physical pixel resolution to a logical (dp) resolution.

```python
utils.logical_resolution(2560, 1600, dpi=200)   # → (2048.0, 1280.0)
```

---

**safe_area_insets**

```python
utils.safe_area_insets(platform: str = "auto") -> SafeAreaInsets
```

Return the safe area insets for a given platform. Safe areas account for notches, home indicators, and status bars. Pass `"auto"` to detect the current OS.

Returns a `SafeAreaInsets` dataclass with `.top`, `.right`, `.bottom`, `.left` (all floats, in dp).

| Platform   | top  | right | bottom | left |
|------------|------|-------|--------|------|
| `ios`      | 44.0 | 0     | 34.0   | 0    |
| `android`  | 24.0 | 0     | 16.0   | 0    |
| `desktop`  | 0    | 0     | 0      | 0    |

```python
insets = utils.safe_area_insets("ios")
print(insets.top, insets.bottom)   # → 44.0  34.0

# Auto-detect current OS
insets = utils.safe_area_insets()
```