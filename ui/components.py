import pygame
from config.settings import (
    BG_COLOR,
    BRUSH_SIZES,
    BRUSH_DROPDOWN_BG,
    BRUSH_DROPDOWN_BORDER,
    BRUSH_SELECTED_COLOR,
    BRUSH_HOVER_COLOR,
    BRUSH_DROPDOWN_RADIUS,
    BRUSH_PADDING,
    BRUSH_ITEM_SPACING,
    BRUSH_HITBOX_PADDING,
    COLOR_INDICATOR_RADIUS,
    COLOR_INDICATOR_PADDING,
    BRUSH_SIZE_SELECTED_COLOR,
    COLOR_INDICATOR_COLOR,
    COLOR_INDICATOR_THICKNESS,
    TOOL_BUTTON_BG,
    TOOL_SELECTED_COLOR,
    HOVER_EASING,
    HOVER_ANIM_DURATION,
    HOVER_FLOAT_OFFSET,
    HOVER_COLOR,
)

class Button:
    def __init__(self, rect, **kwargs):
        self.rect = rect
        self.original_rect = rect.copy()
        self.text = kwargs.get('text', '')
        self.color = kwargs.get('color', TOOL_BUTTON_BG)
        self.text_color = kwargs.get('text_color', (0, 0, 0))
        self.icon = kwargs.get('icon', None)
        self.active = kwargs.get('active', False)
        self.is_tool = kwargs.get('is_tool', False)
        self.is_color = kwargs.get('is_color', False)
        self.is_brush_size = kwargs.get('is_brush_size', False)
        self.is_action = kwargs.get('is_action', False)
        self.current_size = kwargs.get('current_size', BRUSH_SIZES[0])
        self.dropdown_open = False
        self.dropdown_rects = []
        self.hovered_size = None
        self.font = pygame.font.SysFont('Arial', 20)
        self.hover_color = kwargs.get('hover_color', HOVER_COLOR)
        self.float_offset = kwargs.get('float_offset', HOVER_FLOAT_OFFSET)
        
        # Animation properties
        self.hover_progress = 0.0
        self.is_hovered = False
        self.animation_time = 0.0
        self.current_color = self.color
        self.icon_offset = 0

    def update(self, dt):
        # Update animation time
        self.animation_time += dt * (1.0 if self.is_hovered else -1.0)
        self.animation_time = max(0.0, min(self.animation_time, HOVER_ANIM_DURATION))
        
        # Calculate eased progress
        t = self.animation_time / HOVER_ANIM_DURATION
        if HOVER_EASING == "ease_out_quad":
            self.hover_progress = t * (2 - t)
        else:  # linear
            self.hover_progress = t

        # Update visual properties
        self.icon_offset = self.float_offset * self.hover_progress
        
        # Color transition for interactive buttons
        if not self.active and (self.is_tool or self.is_action):
            base_color = TOOL_BUTTON_BG
            self.current_color = [
                base + (self.hover_color[i] - base) * self.hover_progress
                for i, base in enumerate(base_color)
            ]

    def draw(self, surface):
        # Determine background color
        if (self.is_tool or self.is_action) and self.active:
            bg_color = TOOL_SELECTED_COLOR
        else:
            bg_color = self.current_color
        
        # Draw button background
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=5)
        
        # Color selection indicator
        if self.is_color and self.active:
            corners = [
                (self.rect.left + COLOR_INDICATOR_PADDING, self.rect.top + COLOR_INDICATOR_PADDING),
                (self.rect.right - COLOR_INDICATOR_PADDING, self.rect.top + COLOR_INDICATOR_PADDING),
                (self.rect.left + COLOR_INDICATOR_PADDING, self.rect.bottom - COLOR_INDICATOR_PADDING),
                (self.rect.right - COLOR_INDICATOR_PADDING, self.rect.bottom - COLOR_INDICATOR_PADDING)
            ]
            for i, corner in enumerate(corners):
                rect = pygame.Rect(
                    corner[0] - COLOR_INDICATOR_RADIUS,
                    corner[1] - COLOR_INDICATOR_RADIUS,
                    COLOR_INDICATOR_RADIUS * 2,
                    COLOR_INDICATOR_RADIUS * 2
                )
                start_angle = i * 90
                pygame.draw.arc(
                    surface, 
                    COLOR_INDICATOR_COLOR,
                    rect,
                    start_angle * 3.14/180,
                    (start_angle + 90) * 3.14/180,
                    COLOR_INDICATOR_THICKNESS
                )
        
        # Brush size visual indicator
        if self.is_brush_size:
            self._draw_brush_preview(surface)
        
        # Draw dropdown if open
        if self.dropdown_open and self.is_brush_size:
            self._draw_brush_sizes(surface)

        # Draw icon with animation
        if self.icon:
            center = (self.rect.centerx, self.rect.centery + self.icon_offset)
            icon_rect = self.icon.get_rect(center=center)
            surface.blit(self.icon, icon_rect)
        elif self.text:
            self._draw_text(surface)


    def _draw_brush_preview(self, surface):
        # Animated brush size preview
        center_with_offset = (
            self.rect.centerx,
            self.rect.centery + self.icon_offset
        )
        # Draw preview circle
        color = BRUSH_SIZE_SELECTED_COLOR if self.active else (0, 0, 0)
        pygame.draw.circle(
            surface, 
            color,
            center_with_offset,
            self.current_size // 2
        )
        # Animated dropdown indicator
        points = [
            (self.rect.right - 15, center_with_offset[1] - 5),
            (self.rect.right - 10, center_with_offset[1] + 5),
            (self.rect.right - 20, center_with_offset[1] + 5)
        ]
        pygame.draw.polygon(surface, (0, 0, 0), points)

    def _draw_icon(self, surface):
        if self.icon:
            # Apply offset to all icons except brush size
            if not self.is_brush_size:
                icon_center = (self.rect.centerx, self.rect.centery + self.icon_offset)
            else:
                icon_center = self.rect.center
                
            icon_rect = self.icon.get_rect(center=icon_center)
            surface.blit(self.icon, icon_rect)

    def _draw_text(self, surface):
        # Apply offset to tool text only
        if self.is_tool:
            text_center = (self.rect.centerx, self.rect.centery + self.icon_offset)
        else:
            text_center = self.rect.center
            
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=text_center)
        surface.blit(text_surf, text_rect)

    def _draw_brush_sizes(self, surface):
        max_size = max(BRUSH_SIZES)
        dropdown_width = max_size + BRUSH_PADDING * 2
        dropdown_height = sum(size + BRUSH_ITEM_SPACING for size in BRUSH_SIZES) + BRUSH_PADDING
        
        dropdown_rect = pygame.Rect(
            self.rect.x - (dropdown_width - self.rect.width) // 2,
            self.rect.y - dropdown_height - 10,
            dropdown_width,
            dropdown_height
        )
        
        # Draw dropdown background
        pygame.draw.rect(surface, BRUSH_DROPDOWN_BG, dropdown_rect, border_radius=BRUSH_DROPDOWN_RADIUS)
        pygame.draw.rect(surface, BRUSH_DROPDOWN_BORDER, dropdown_rect, 2, border_radius=BRUSH_DROPDOWN_RADIUS)
        
        self.dropdown_rects = []
        y_offset = BRUSH_PADDING
        mouse_pos = pygame.mouse.get_pos()
        self.hovered_size = None
        
        for size in BRUSH_SIZES:
            # Actual circle position
            circle_pos = (
                dropdown_rect.centerx,
                dropdown_rect.y + y_offset + size//2
            )
            
            # Clickable area (larger than the circle)
            hitbox_rect = pygame.Rect(
                dropdown_rect.centerx - max_size//2 - BRUSH_HITBOX_PADDING,
                dropdown_rect.y + y_offset - BRUSH_HITBOX_PADDING,
                max_size + BRUSH_HITBOX_PADDING*2,
                size + BRUSH_HITBOX_PADDING*2
            )
            self.dropdown_rects.append(hitbox_rect)
            
            # Check hover state
            is_hovered = hitbox_rect.collidepoint(mouse_pos)
            if is_hovered:
                self.hovered_size = size
            
            # Selected highlight
            if size == self.current_size:
                highlight_rect = pygame.Rect(
                    dropdown_rect.x + 5,
                    dropdown_rect.y + y_offset - 5,
                    dropdown_rect.width - 10,
                    size + 10
                )
                pygame.draw.rect(surface, BRUSH_SELECTED_COLOR, highlight_rect, border_radius=5)
            # Hover highlight (only if not selected)
            elif is_hovered:
                hover_rect = pygame.Rect(
                    dropdown_rect.x + 10,
                    dropdown_rect.y + y_offset,
                    dropdown_rect.width - 20,
                    size
                )
                pygame.draw.rect(surface, BRUSH_HOVER_COLOR, hover_rect, border_radius=4)
            
            # Draw the brush size circle
            pygame.draw.circle(
                surface,
                (0, 0, 0),
                circle_pos,
                size // 2
            )
            
            y_offset += size + BRUSH_ITEM_SPACING