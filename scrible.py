import pygame
import random
from collections import deque
from pygame.locals import *

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Drawing Guessing Game")

# Load tool icons
try:
    brush_icon = pygame.image.load('brush.png').convert_alpha()
    eraser_icon = pygame.image.load('eraser.png').convert_alpha()
    fill_icon = pygame.image.load('fill.png').convert_alpha()
    # Resize icons to 60x60 pixels
    brush_icon = pygame.transform.scale(brush_icon, (60, 60))
    eraser_icon = pygame.transform.scale(eraser_icon, (60, 60))
    fill_icon = pygame.transform.scale(fill_icon, (60, 60))
except FileNotFoundError as e:
    print(f"Error loading icon files: {e}")
    pygame.quit()
    exit()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BG_COLOR = (240, 240, 240)
COLORS = [
    BLACK,         # 0 - Black
    RED,           # 1 - Red
    (0, 255, 0),   # 2 - Green
    (0, 0, 255),   # 3 - Blue
    (255, 255, 0), # 4 - Yellow
    (255, 165, 0), # 5 - Orange
    (128, 0, 128), # 6 - Purple
    (255, 192, 203)# 7 - Pink
]

# Drawing parameters
BRUSH_SIZES = [2, 5, 10, 15, 20]
current_brush_size = BRUSH_SIZES[2]
brush_color = COLORS[0]
fill_color = COLORS[1]
drawing = False
last_pos = None
tool = "brush"  # brush, eraser, fill

# Undo/redo stacks
undo_stack = deque(maxlen=20)
redo_stack = deque(maxlen=20)

# Canvas setup
canvas = pygame.Surface((1600, 900))
canvas.fill(WHITE)
undo_stack.append(canvas.copy())

# UI dimensions
TOOLBAR_WIDTH = 200
PALETTE_SIZE = 40
BUTTON_HEIGHT = 50

class Button:
    def __init__(self, rect, text, color, text_color=WHITE, is_tool=False, icon=None):
        self.rect = rect
        self.text = text
        self.color = color
        self.text_color = text_color
        self.is_tool = is_tool
        self.active = False
        self.icon = icon
        
    def draw(self, surface):
        # Draw active state
        if self.is_tool and self.active:
            pygame.draw.rect(surface, BLACK, self.rect.inflate(4, 4), 3, border_radius=10)
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        
        # Draw icon if available
        if self.icon:
            icon_rect = self.icon.get_rect(center=self.rect.center)
            surface.blit(self.icon, icon_rect)
        else:
            font = pygame.font.SysFont('Arial', 20)
            text_surf = font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

def create_tools():
    tools = []
    y = 50
    
    # Tool buttons with icons
    tools.append(Button(
        pygame.Rect(WIDTH - TOOLBAR_WIDTH + 20, y, 80, 80),
        "brush", BG_COLOR, BLACK, True, brush_icon
    ))
    y += 100
    
    tools.append(Button(
        pygame.Rect(WIDTH - TOOLBAR_WIDTH + 20, y, 80, 80),
        "eraser", BG_COLOR, BLACK, True, eraser_icon
    ))
    y += 100
    
    tools.append(Button(
        pygame.Rect(WIDTH - TOOLBAR_WIDTH + 20, y, 80, 80),
        "fill", BG_COLOR, BLACK, True, fill_icon
    ))
    y += 150
    
    # Color palette
    for i, color in enumerate(COLORS):
        tools.append(Button(
            pygame.Rect(WIDTH - TOOLBAR_WIDTH + 10 + (i%2)*60, y + (i//2)*60, 50, 50),
            "", color, is_tool=True
        ))
    y += 180
    
    # Brush sizes
    for i, size in enumerate(BRUSH_SIZES):
        tools.append(Button(
            pygame.Rect(WIDTH - TOOLBAR_WIDTH + 10 + (i%2)*60, y + (i//2)*60, 50, 50),
            str(size), BG_COLOR, BLACK, is_tool=True
        ))
    y += 150
    
    # Undo/redo
    tools.append(Button(
        pygame.Rect(WIDTH - TOOLBAR_WIDTH + 10, HEIGHT-120, 80, 50),
        "Undo", BG_COLOR, BLACK
    ))
    tools.append(Button(
        pygame.Rect(WIDTH - TOOLBAR_WIDTH + 100, HEIGHT-120, 80, 50),
        "Redo", BG_COLOR, BLACK
    ))
    
    return tools

tools = create_tools()

def scanline_fill(surface, start_pos, new_color):
    """Optimized flood fill using scanline algorithm"""
    old_color = surface.get_at(start_pos)
    if old_color == new_color:
        return
    
    surface.lock()
    x, y = start_pos
    w, h = surface.get_size()
    
    stack = deque()
    stack.append((x, y))
    
    while stack:
        x, y = stack.pop()
        while x >= 0 and surface.get_at((x, y)) == old_color:
            x -= 1
        x += 1
        span_above = span_below = False
        
        while x < w and surface.get_at((x, y)) == old_color:
            surface.set_at((x, y), new_color)
            
            if not span_above and y > 0 and surface.get_at((x, y-1)) == old_color:
                stack.append((x, y-1))
                span_above = True
            elif span_above and y > 0 and surface.get_at((x, y-1)) != old_color:
                span_above = False
                
            if not span_below and y < h-1 and surface.get_at((x, y+1)) == old_color:
                stack.append((x, y+1))
                span_below = True
            elif span_below and y < h-1 and surface.get_at((x, y+1)) != old_color:
                span_below = False
                
            x += 1
    surface.unlock()

def handle_drawing(event):
    global last_pos, undo_stack, redo_stack
    
    if event.type == MOUSEBUTTONDOWN and event.button == 1:
        x, y = event.pos
        for btn in tools:
            if btn.rect.collidepoint(x, y):
                handle_tool_click(btn)
                return
                
        if canvas.get_rect(topleft=(20, 20)).collidepoint(x-20, y-20):
            save_state()
            if tool == "fill":
                scanline_fill(canvas, (x-20, y-20), fill_color)
            else:
                global drawing
                drawing = True
                last_pos = (x-20, y-20)
    
    elif event.type == MOUSEBUTTONUP and event.button == 1:
        drawing = False
        last_pos = None
    
    elif event.type == MOUSEMOTION and drawing:
        x, y = event.pos
        current_pos = (x-20, y-20)
        if last_pos:
            if tool == "brush":
                pygame.draw.line(canvas, brush_color, last_pos, current_pos, current_brush_size)
            elif tool == "eraser":
                pygame.draw.line(canvas, WHITE, last_pos, current_pos, current_brush_size)
            last_pos = current_pos

def handle_tool_click(btn):
    global current_brush_size, tool, brush_color, fill_color
    
    for t in tools:
        if t.is_tool:
            t.active = False
    
    if btn.text == "brush":
        tool = "brush"
        btn.active = True
    elif btn.text == "eraser":
        tool = "eraser"
        btn.active = True
    elif btn.text == "fill":
        tool = "fill"
        btn.active = True
    elif btn.text == "Undo":
        if len(undo_stack) > 1:
            redo_stack.append(undo_stack.pop())
            canvas.blit(undo_stack[-1], (0, 0))
    elif btn.text == "Redo":
        if redo_stack:
            undo_stack.append(redo_stack.pop())
            canvas.blit(undo_stack[-1], (0, 0))
    elif btn.text.isdigit():
        current_brush_size = int(btn.text)
        btn.active = True
    elif btn.color in COLORS:
        if tool == "fill":
            fill_color = btn.color
        else:
            brush_color = btn.color
        btn.active = True

def save_state():
    undo_stack.append(canvas.copy())
    redo_stack.clear()

# Game loop
running = True
clock = pygame.time.Clock()
status_font = pygame.font.SysFont('Arial', 24)

while running:
    screen.fill(BG_COLOR)
    
    # Draw canvas area
    screen.blit(canvas, (20, 20))
    pygame.draw.rect(screen, BLACK, (20, 20, 1600, 900), 2)
    
    # Draw toolbar
    pygame.draw.rect(screen, BG_COLOR, (WIDTH - TOOLBAR_WIDTH, 0, TOOLBAR_WIDTH, HEIGHT))
    for btn in tools:
        btn.draw(screen)
    
    # Draw status indicators
    pygame.draw.rect(screen, BLACK, (WIDTH-180, HEIGHT-280, 60, 60))
    pygame.draw.rect(screen, brush_color, (WIDTH-175, HEIGHT-275, 50, 50))
    pygame.draw.rect(screen, BLACK, (WIDTH-110, HEIGHT-280, 60, 60))
    pygame.draw.rect(screen, fill_color, (WIDTH-105, HEIGHT-275, 50, 50))
    
    size_text = status_font.render(f"Size: {current_brush_size}", True, BLACK)
    screen.blit(size_text, (WIDTH-180, HEIGHT-200))
    
    # Handle events
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        handle_drawing(event)
    
    # Draw cursor circle
    mouse_pos = pygame.mouse.get_pos()
    canvas_rect = pygame.Rect(20, 20, 1600, 900)
    if canvas_rect.collidepoint(mouse_pos):
        radius = current_brush_size // 2
        if tool == "eraser":
            color = RED
        elif tool == "fill":
            color = fill_color
        else:
            color = brush_color
        
        # Draw transparent circle
        cursor_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(cursor_surface, (*color, 100), (radius, radius), radius)
        screen.blit(cursor_surface, (mouse_pos[0]-radius, mouse_pos[1]-radius))
        # Draw outline
        pygame.draw.circle(screen, color, mouse_pos, radius, 2)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()