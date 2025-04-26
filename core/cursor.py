# core/cursor.py
import pygame
from config.settings import TOOL_ICON_SIZE, COLORS

def draw_enhanced_cursor(screen, tool_state, mouse_pos, icons):
    """Draw tool-specific cursor with consistent icon positioning"""
    cursor_x_offset = -4
    cursor_y_offset = -50
    icon_size = TOOL_ICON_SIZE[0]  # Assuming square icons
    
    # For fill tool
    if tool_state.active_tool == 'fill':
        # Draw bucket icon
        bucket_icon = pygame.transform.scale(icons['fill'], (icon_size, icon_size))
        icon_pos = (
            mouse_pos[0] + cursor_x_offset,
            mouse_pos[1] + cursor_y_offset
        )
        screen.blit(bucket_icon, icon_pos)
        
        # Add crosshair for precision
        pygame.draw.line(screen, (0,0,0), (mouse_pos[0]-8, mouse_pos[1]), (mouse_pos[0]+8, mouse_pos[1]), 1)
        pygame.draw.line(screen, (0,0,0), (mouse_pos[0], mouse_pos[1]-8), (mouse_pos[0], mouse_pos[1]+8), 1)
        return

    # For brush/eraser
    radius = tool_state.brush_size // 2
    color = (255,0,0) if tool_state.active_tool == 'eraser' else tool_state.brush_color
    
    # Draw translucent preview
    preview_surf = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    pygame.draw.circle(preview_surf, (*color, 100), (radius, radius), radius)
    screen.blit(preview_surf, (mouse_pos[0]-radius, mouse_pos[1]-radius))
    
    # Draw outline
    pygame.draw.circle(screen, color, mouse_pos, radius, 1)
    
    # Draw tool icon (top-right of cursor)
    tool_icon = icons['brush' if tool_state.active_tool == 'brush' else 'eraser']
    scaled_icon = pygame.transform.scale(tool_icon, (icon_size, icon_size))
    screen.blit(scaled_icon, (
        mouse_pos[0] + cursor_x_offset,
        mouse_pos[1] + cursor_y_offset
    ))