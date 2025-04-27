# config/settings.py
# ------------------
# Display Configuration
INITIAL_WIDTH = 1280
INITIAL_HEIGHT = 600
ASPECT_RATIO = 16/9
BG_COLOR = (240, 240, 240)

# Canvas Configuration
CANVAS_SIZE = (1700, 900)          # Internal drawing resolution
CANVAS_MARGIN = 20                 # Space around canvas in window
CANVAS_DISPLAY_COLOR = (255, 255, 255)  # Canvas background color

# Tool Configuration
# -----------------
# Brush Settings
BRUSH_SIZES = [7, 14, 21, 28, 35]
DEFAULT_BRUSH_INDEX = 0
TOOL_ICON_SIZE = (80, 80)

# Brush Dropdown Settings
BRUSH_DROPDOWN_BG = (240, 240, 240)
BRUSH_DROPDOWN_BORDER = (200, 200, 200)
BRUSH_SELECTED_COLOR = (220, 230, 255)
BRUSH_HOVER_COLOR = (240, 245, 255)
BRUSH_DROPDOWN_RADIUS = 8
BRUSH_PADDING = 20
BRUSH_ITEM_SPACING = 25
BRUSH_HITBOX_PADDING = 0
BRUSH_SIZE_SELECTED_COLOR = (128, 0, 128)  # Purple
BRUSH_SIZE_HOVER_COLOR = (200, 200, 200)    # Grey

# Color Configuration
# ------------------
COLORS = [
    (255, 255, 255), (193, 193, 193), (239, 19, 11), (255, 113, 0),
    (255, 228, 0), (0, 204, 0), (1, 255, 145), (0, 178, 255),
    (35, 31, 211), (163, 0, 186), (223, 105, 167), (255, 172, 142),
    (160, 82, 45), (0, 0, 0), (80, 80, 80), (116, 11, 7),
    (194, 56, 0), (232, 162, 0), (0, 70, 25), (0, 120, 93),
    (0, 86, 158), (14, 8, 101), (85, 0, 105), (135, 53, 84),
    (204, 119, 77), (99, 48, 13)
]

# Color Palette Settings
COLOR_BUTTON_SIZE = 40     # Size of each color square
COLOR_BUTTON_SPACING = 5   # Space between color buttons
COLOR_ROWS = 2             # Number of color rows
COLORS_PER_ROW = 13        # Colors per row
PALETTE_BOTTOM_MARGIN = 5 # Space between palette and window bottom
PALETTE_VERTICAL_SPACING = 10  # Space between color rows

# Color Indicator Settings
COLOR_INDICATOR_RADIUS = 6
COLOR_INDICATOR_PADDING = 5
COLOR_INDICATOR_COLOR = (100, 180, 255)
COLOR_INDICATOR_THICKNESS = 2

# Toolbar Configuration
# --------------------
TOOL_BUTTON_SIZE = 80           # Size of tool buttons
TOOL_SPACING = 30               # Horizontal space between tools
BRUSH_SIZE_BUTTON_SIZE = 80     # Brush size selector button size
PALETTE_TOOL_PADDING = 60       # Space between palette and first tool
TOOL_BUTTON_RADIUS = 8          # Rounded corners radius
BUTTON_HIGHLIGHT_COLOR = (180, 180, 255)

# Tool Appearance
TOOL_BUTTON_BG = (255, 255, 255)  # White background
TOOL_SELECTED_COLOR = (128, 0, 128)  # Purple (#800080)

# Animation Settings
HOVER_ANIM_DURATION = 0.2  # seconds
HOVER_FLOAT_OFFSET = -5     # pixels (negative for upward float)
HOVER_COLOR = (230, 230, 230)  # Light gray hover color
HOVER_EASING = "ease_out_quad"  # or "linear" 

# Action Buttons
ACTION_BUTTON_WIDTH = 80
ACTION_BUTTON_HEIGHT = 80
ACTION_BUTTON_SPACING = 20 # Vertical spacing
ACTION_RIGHT_MARGIN = 80   # Space from right window edge

# Cursor & Icons
# --------------
ICON_PATHS = {
    'brush': 'assets/icons/brush.png',
    'eraser': 'assets/icons/eraser.png',
    'fill': 'assets/icons/fill.png',
    'undo': 'assets/icons/undo.png',
    'redo': 'assets/icons/redo.png',
    'clear': 'assets/icons/clear.png'
}
CURSOR_PREVIEW_ALPHA = 100  # Translucency (0-255)