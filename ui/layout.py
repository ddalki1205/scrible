# ui/layout.py
import pygame
from ui.components import Button
from config.settings import (
    # Add these new imports
    TOOL_BUTTON_BG,
    TOOL_SELECTED_COLOR,
    # Keep existing imports
    COLOR_BUTTON_SIZE, COLOR_BUTTON_SPACING, COLOR_ROWS, COLORS_PER_ROW,
    PALETTE_BOTTOM_MARGIN, PALETTE_VERTICAL_SPACING, TOOL_BUTTON_SIZE,
    TOOL_SPACING, BRUSH_SIZE_BUTTON_SIZE, PALETTE_TOOL_PADDING,
    ACTION_BUTTON_WIDTH, ACTION_BUTTON_HEIGHT, ACTION_BUTTON_SPACING,
    ACTION_RIGHT_MARGIN, CANVAS_MARGIN,
    TOOL_BUTTON_RADIUS, BUTTON_HIGHLIGHT_COLOR,
    COLORS, ICON_PATHS, BRUSH_SIZES
)

def create_tools(window_size, icons):
    win_w, win_h = window_size
    tools = []

    # Calculate palette dimensions
    palette_width = COLORS_PER_ROW * (COLOR_BUTTON_SIZE + COLOR_BUTTON_SPACING) - COLOR_BUTTON_SPACING
    total_tools_width = (
        BRUSH_SIZE_BUTTON_SIZE + 
        3 * TOOL_BUTTON_SIZE + 
        3 * TOOL_SPACING
    )
    start_x = (win_w - (palette_width + PALETTE_TOOL_PADDING + total_tools_width)) // 2

    # Color Palette (two rows at bottom)
    palette_y = win_h - (COLOR_ROWS * (COLOR_BUTTON_SIZE + PALETTE_VERTICAL_SPACING)) - PALETTE_BOTTOM_MARGIN

    # First color row
    for i in range(COLORS_PER_ROW):
        tools.append({
            'type': 'color',
            'color': COLORS[i],
            'button': Button(
                pygame.Rect(
                    start_x + i*(COLOR_BUTTON_SIZE + COLOR_BUTTON_SPACING),
                    palette_y,
                    COLOR_BUTTON_SIZE,
                    COLOR_BUTTON_SIZE
                ),
                color=COLORS[i],
                is_color=True,
                border_radius=TOOL_BUTTON_RADIUS
            )
        })

    # Second color row
    for i in range(COLORS_PER_ROW):
        tools.append({
            'type': 'color',
            'color': COLORS[i+13],
            'button': Button(
                pygame.Rect(
                    start_x + i*(COLOR_BUTTON_SIZE + COLOR_BUTTON_SPACING),
                    palette_y + COLOR_BUTTON_SIZE + PALETTE_VERTICAL_SPACING,
                    COLOR_BUTTON_SIZE,
                    COLOR_BUTTON_SIZE
                ),
                color=COLORS[i+13],
                is_color=True,
                border_radius=TOOL_BUTTON_RADIUS
            )
        })

    # Tools Section (right of palette)
    tools_start_x = start_x + palette_width + PALETTE_TOOL_PADDING
    tools_y = palette_y + (COLOR_BUTTON_SIZE // 2)

    # Brush Size Selector
    tools.append({
        'type': 'brush_size',
        'button': Button(
            pygame.Rect(tools_start_x, tools_y, BRUSH_SIZE_BUTTON_SIZE, BRUSH_SIZE_BUTTON_SIZE),
            is_brush_size=True,
            current_size=BRUSH_SIZES[0],
            color=TOOL_BUTTON_BG,
            border_radius=TOOL_BUTTON_RADIUS
        )
    })

    # Tools in horizontal layout
    tool_positions = [
        (tools_start_x + BRUSH_SIZE_BUTTON_SIZE + TOOL_SPACING, 'brush'),
        (tools_start_x + BRUSH_SIZE_BUTTON_SIZE + TOOL_SPACING*2 + TOOL_BUTTON_SIZE, 'fill'),
        (tools_start_x + BRUSH_SIZE_BUTTON_SIZE + TOOL_SPACING*3 + TOOL_BUTTON_SIZE*2, 'eraser')
    ]

    for x, name in tool_positions:
        tools.append({
            'type': 'tool',
            'name': name,
            'button': Button(
                pygame.Rect(x, tools_y, TOOL_BUTTON_SIZE, TOOL_BUTTON_SIZE),
                icon=icons[name],
                is_tool=True,
                color=TOOL_BUTTON_BG,  # Base white color
                # Selection color handled by Button class logic
                border_radius=TOOL_BUTTON_RADIUS
            )
        })

    # Action Buttons (top right)
    action_x = win_w - ACTION_BUTTON_WIDTH - ACTION_RIGHT_MARGIN
    action_y = CANVAS_MARGIN
    
    actions = ['undo', 'redo', 'clear']
    for i, action in enumerate(actions):
        tools.append({
            'type': 'action',
            'name': action,
            'button': Button(
                pygame.Rect(
                    action_x,
                    action_y + i*(ACTION_BUTTON_HEIGHT + ACTION_BUTTON_SPACING),
                    ACTION_BUTTON_WIDTH,
                    ACTION_BUTTON_HEIGHT
                ),
                text=action.capitalize(),
                color=(255, 100, 100) if action == 'clear' else BUTTON_HIGHLIGHT_COLOR,
                border_radius=TOOL_BUTTON_RADIUS
            )
        })

    return tools