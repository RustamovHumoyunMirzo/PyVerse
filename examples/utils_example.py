from pyverse import utils

# Unit conversions
print(utils.pxToDp(32, dpi=320))         # 16.0
print(utils.dpToPx(16, dpi=320))         # 32.0
print(utils.remToPx(1.5))                # 24.0
print(utils.ptToPx(12))                  # 16.0
print(utils.vwToPx(50, 1920))            # 960.0

# Color
print(utils.hex_to_rgb("#FF5733"))        # (255, 87, 51)
print(utils.lighten("#FF5733", 0.2))      # brighter variant
print(utils.contrast_ratio("#fff", "#000")) # 21.0
print(utils.is_accessible("#767676", "#fff")) # True (AA)

# Layout math
print(utils.clamp(150, 0, 100))           # 100
print(utils.lerp(0, 100, 0.25))           # 25.0
print(utils.grid_columns(1200, 300, 16))  # 3
print(utils.breakpoint(900))              # 'lg'

# Platform
dpi = utils.screen_dpi()
print(utils.is_mobile_density(dpi))
print(utils.logical_resolution(2560, 1600, dpi=200))
insets = utils.safe_area_insets("ios")
print(insets.top, insets.bottom)          # 44.0  34.0