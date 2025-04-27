import pygame
import traceback
import time
from pygame.locals import *
from config.settings import *
from core.canvas import CanvasManager
from core.state import ToolState
from ui.layout import create_tools
from utils.helpers import load_icons, handle_resize
from core.cursor import draw_enhanced_cursor
from core.event_handlers import (
    handle_resize_event,
    handle_mouse_down,
    handle_mouse_motion
)
from core.interface import draw_interface

def main():
    try:
        pygame.init()
        screen = pygame.display.set_mode((INITIAL_WIDTH, INITIAL_HEIGHT), RESIZABLE)
        pygame.display.set_caption("Group 6 Scribbl.io")
        
        # Initialize components
        tool_state = ToolState()
        icons = load_icons()
        current_size = (INITIAL_WIDTH, INITIAL_HEIGHT)
        tools = create_tools(current_size, icons)
        canvas_area = pygame.Rect(20, 20, current_size[0]-240, current_size[1]-140)
        canvas_manager = CanvasManager()

        # Background handling variables
        background_image = None
        scaled_background = None
        
        # Load background image
        try:
            background_image = pygame.image.load("assets/bg.png").convert()
            # Initial scale to window size
            scaled_background = pygame.transform.smoothscale(background_image, current_size)
        except Exception as e:
            print(f"Couldn't load background image: {e}")
            # Fallback: create solid background surface
            scaled_background = pygame.Surface(current_size)
            scaled_background.fill(BG_COLOR)

        clock = pygame.time.Clock()
        running = True
        drawing = False
        last_time = time.time()

        while running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            # Update animations
            for item in tools:
                btn = item['button']
                if item['type'] in ['tool', 'brush_size']:
                    btn.update(dt)

            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    continue
                
                if event.type == VIDEORESIZE:
                    current_size = (event.w, event.h)
                    screen = pygame.display.set_mode(current_size, RESIZABLE)
                    
                    # Handle background scaling (aspect fill)
                    if background_image:
                        # Calculate aspect-preserving scale to fill screen
                        screen_w, screen_h = current_size
                        img_w, img_h = background_image.get_size()
                        
                        width_ratio = screen_w / img_w
                        height_ratio = screen_h / img_h
                        scale = max(width_ratio, height_ratio)
                        
                        scaled_size = (int(img_w * scale), (int(img_h * scale)))
                        scaled_background = pygame.transform.smoothscale(background_image, scaled_size)
                        
                        # Crop to center
                        scaled_background = scaled_background.subsurface(
                            (scaled_size[0] - screen_w) // 2,
                            (scaled_size[1] - screen_h) // 2,
                            screen_w,
                            screen_h
                        )
                    else:
                        scaled_background = pygame.Surface(current_size)
                        scaled_background.fill(BG_COLOR)
                    
                    # Update UI elements
                    tools, canvas_area = handle_resize(event.w, event.h, tools, icons)
                
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    drawing = handle_mouse_down(event, tools, tool_state, canvas_manager, canvas_area)
                    continue
                
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    drawing = False
                    canvas_manager.save_state()
                    tool_state.last_pos = None
                    continue
                
                if event.type == MOUSEMOTION:
                    # Update hover states for all interactive elements
                    mouse_pos = event.pos
                    for item in tools:
                        btn = item['button']
                        if item['type'] in ['tool', 'brush_size', 'action']:  # Added 'action'
                            btn.is_hovered = btn.original_rect.collidepoint(mouse_pos)
                    
                    if drawing:
                        handle_mouse_motion(event, drawing, tool_state, canvas_manager, canvas_area)

           # Draw everything
            screen.blit(scaled_background, (0, 0))  # Draw background first
            draw_interface(
                screen, 
                canvas_manager, 
                tools, 
                tool_state, 
                canvas_area, 
                icons, 
                draw_enhanced_cursor
            )
            
            pygame.display.flip()
            clock.tick(60)

    except Exception as e:
        traceback.print_exc()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()