# core/interface.py
import pygame
from config.settings import BG_COLOR

def draw_interface(screen, canvas_manager, tools, tool_state, canvas_area, icons, 
                  draw_enhanced_cursor, background_image=None):
    
    # Draw canvas
    scaled_canvas = pygame.transform.smoothscale(
        canvas_manager.surface, 
        (canvas_area.width, canvas_area.height)
    )
    screen.blit(scaled_canvas, canvas_area.topleft)
    pygame.draw.rect(screen, (0, 0, 0), canvas_area, 2)
    
    # Update color button states
    for item in tools:
        if item['type'] == 'color':
            current_color = tool_state.brush_color
            item['button'].active = (item['color'] == current_color)
            
        item['button'].draw(screen)
    
    
    # Draw cursor
    mouse_pos = pygame.mouse.get_pos()
    if canvas_area.collidepoint(mouse_pos):
        draw_enhanced_cursor(screen, tool_state, mouse_pos, icons)
    
    pygame.display.flip()