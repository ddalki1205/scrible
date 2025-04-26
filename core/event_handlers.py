# core/event_handlers.py
import pygame
from config.settings import CANVAS_SIZE, COLORS, BRUSH_SIZES, CANVAS_MARGIN

def handle_resize_event(event, screen, current_size, tools, canvas_area, handle_resize):
    screen, w, h = handle_resize(event, screen)
    current_size = (w, h)
    
    # Calculate canvas area (uses 80% of vertical space)
    canvas_height = int(h * 0.8) - CANVAS_MARGIN*2
    canvas_area.update(
        CANVAS_MARGIN,
        CANVAS_MARGIN,
        w - CANVAS_MARGIN*2,
        canvas_height
    )
    
    return current_size, tools, canvas_area
    
    return current_size, tools, canvas_area
def handle_brush_size_click(item, mouse_pos, tool_state):
    btn = item['button']
    
    # Check if clicked on dropdown items
    if btn.dropdown_open:
        for i, rect in enumerate(btn.dropdown_rects):
            # Create a slightly larger hitbox for easier clicking
            hitbox = rect.inflate(10, 10)
            if hitbox.collidepoint(mouse_pos):
                tool_state.brush_size = BRUSH_SIZES[i]
                btn.current_size = BRUSH_SIZES[i]
                btn.dropdown_open = False
                return True
    
    # Toggle dropdown if clicked on main button
    if btn.rect.collidepoint(mouse_pos):
        btn.dropdown_open = not btn.dropdown_open
        return True
    
    # Clicked outside - close dropdown
    btn.dropdown_open = False
    return False

def handle_mouse_down(event, tools, tool_state, canvas_manager, canvas_area):
    mouse_pos = event.pos
    clicked_ui = False
    
    for item in tools:
        btn = item['button']
        if btn.rect.collidepoint(mouse_pos) or (hasattr(btn, 'dropdown_open') and btn.dropdown_open):
            clicked_ui = True
            if item['type'] == 'brush_size':
                handle_brush_size_click(item, mouse_pos, tool_state)
            else:
                handle_ui_click(item, tool_state, tools, canvas_manager)
            break

    if not clicked_ui and canvas_area.collidepoint(mouse_pos):
        handle_canvas_click(mouse_pos, tool_state, canvas_manager, canvas_area)
        
        # Only create initial dot for brush/eraser
        if tool_state.active_tool in ['brush', 'eraser']:
            x = int((mouse_pos[0] - canvas_area.left) * CANVAS_SIZE[0] / canvas_area.width)
            y = int((mouse_pos[1] - canvas_area.top) * CANVAS_SIZE[1] / canvas_area.height)
            color = tool_state.brush_color if tool_state.active_tool == 'brush' else COLORS[1]
            pygame.draw.circle(
                canvas_manager.surface,
                color,
                (x, y),
                tool_state.brush_size // 2
            )
            tool_state.last_pos = (x, y)
            return True  # Drawing started
    return False

def handle_ui_click(item, tool_state, tools, canvas_manager):
    if item['type'] == 'tool':
        # Update active tool
        tool_state.active_tool = item['name']
        # Toggle button states
        for other in tools:
            if other['type'] == 'tool':
                other['button'].active = (other == item)
                
    elif item['type'] == 'color':
        # Update color for all tools
        tool_state.brush_color = item['color']
            
    elif item['type'] == 'action':
        action_handlers = {
            'undo': canvas_manager.handle_undo,
            'redo': canvas_manager.handle_redo,
            'clear': canvas_manager.clear
        }
        action_handlers[item['name']]()

def handle_canvas_click(mouse_pos, tool_state, canvas_manager, canvas_area):
    x = int((mouse_pos[0] - canvas_area.left) * CANVAS_SIZE[0] / canvas_area.width)
    y = int((mouse_pos[1] - canvas_area.top) * CANVAS_SIZE[1] / canvas_area.height)
    
    if tool_state.active_tool == 'fill':
        canvas_manager.flood_fill((x, y), tool_state.brush_color)
    else:
        tool_state.last_pos = (x, y)

def handle_mouse_motion(event, drawing, tool_state, canvas_manager, canvas_area):
    if not drawing or tool_state.active_tool not in ['brush', 'eraser']:
        return
    
    mouse_pos = event.pos
    if not canvas_area.collidepoint(mouse_pos):
        return
    
    # Convert to canvas coordinates
    x = int((mouse_pos[0] - canvas_area.left) * CANVAS_SIZE[0] / canvas_area.width)
    y = int((mouse_pos[1] - canvas_area.top) * CANVAS_SIZE[1] / canvas_area.height)
    
    if tool_state.last_pos:
        color = tool_state.brush_color if tool_state.active_tool == 'brush' else COLORS[1]
        radius = tool_state.brush_size // 2
        
        # Calculate distance between points
        dx = x - tool_state.last_pos[0]
        dy = y - tool_state.last_pos[1]
        distance = max(abs(dx), abs(dy))
        
        # Interpolate points based on brush size
        step = max(1, radius // 2)
        steps = max(1, int(distance / step))
        
        for i in range(steps + 1):
            t = i / steps
            px = int(tool_state.last_pos[0] + dx * t)
            py = int(tool_state.last_pos[1] + dy * t)
            pygame.draw.circle(
                canvas_manager.surface,
                color,
                (px, py),
                radius
            )
    
    tool_state.last_pos = (x, y)