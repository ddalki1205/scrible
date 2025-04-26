import pygame
from config.settings import ASPECT_RATIO, INITIAL_WIDTH, INITIAL_HEIGHT, TOOL_ICON_SIZE, ICON_PATHS
from ui.layout import *

def handle_resize(new_width, new_height, tools, icons):
    """Update UI elements positions after resize"""
    # Recreate tools with new positions
    new_tools = create_tools((new_width, new_height), icons)
    
    # Update canvas area (maintain 20px margins)
    canvas_area = pygame.Rect(
        20, 
        20, 
        new_width - 240,  # 240 = 200 tools + 20*2 margins
        new_height - 140  # 140 = 100 bottom UI + 20*2 margins
    )
    
    return new_tools, canvas_area

def load_icons():
    icons = {}
    for tool_type, path in ICON_PATHS.items():
        try:
            icon = pygame.image.load(path).convert_alpha()
            icons[tool_type] = pygame.transform.scale(icon, TOOL_ICON_SIZE)
        except FileNotFoundError:
            icons[tool_type] = pygame.Surface(TOOL_ICON_SIZE)
            icons[tool_type].fill((200, 200, 200))  # Fallback gray
    return icons