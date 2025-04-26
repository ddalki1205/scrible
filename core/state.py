# core/state.py
from config.settings import BRUSH_SIZES, DEFAULT_BRUSH_INDEX, COLORS

class ToolState:
    def __init__(self):
        self.active_tool = 'brush'
        self.brush_color = COLORS[0]  # Shared color for all tools
        self.brush_size = BRUSH_SIZES[DEFAULT_BRUSH_INDEX]
        self.last_pos = None

    def update_tool(self, tool):
        self.active_tool = tool