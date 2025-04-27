from collections import deque
import pygame
import hashlib
from config.settings import CANVAS_SIZE, COLORS

class CanvasManager:
    def __init__(self):
        self.surface = pygame.Surface(CANVAS_SIZE, pygame.SRCALPHA)
        self.surface.fill(COLORS[0])
        self.undo_stack = deque(maxlen=20)
        self.redo_stack = deque(maxlen=20)
        self.save_state()

    def save_state(self):
        """Save current canvas state to undo stack if different from last"""
        current_hash = self.get_surface_hash()
        if not self.undo_stack or current_hash != self.undo_stack[-1][1]:
            self.undo_stack.append((self.surface.copy(), current_hash))
            self.redo_stack.clear()

    def handle_undo(self):
        """Revert to previous state"""
        if len(self.undo_stack) > 1:
            current_state = self.undo_stack.pop()
            self.redo_stack.append(current_state)
            self.surface.blit(self.undo_stack[-1][0], (0, 0))

    def handle_redo(self):
        """Reapply next state"""
        if self.redo_stack:
            redo_state = self.redo_stack.pop()
            self.undo_stack.append(redo_state)
            self.surface.blit(redo_state[0], (0, 0))

    def get_surface_hash(self):
        """Create hash of surface pixels for comparison"""
        return hashlib.md5(pygame.image.tostring(self.surface, "RGB")).hexdigest()

    def clear(self):
        """Clear canvas while preserving history"""
        self.save_state()
        self.surface.fill(COLORS[0])

    def get_scaled(self, target_size):
        """Return scaled version of canvas"""
        return pygame.transform.smoothscale(self.surface, target_size)
    
    def flood_fill(self, pos, color):
        """Optimized flood fill using PixelArray and scanline algorithm"""
        try:
            old_color = self.surface.get_at(pos)
        except IndexError:
            return  # Clicked outside canvas
        
        if old_color == color:
            return

        # Convert colors to mapped integer format for faster comparison
        old_rgb = self.surface.map_rgb(old_color)
        new_rgb = self.surface.map_rgb(color)
        
        q = deque()
        q.append(pos)
        width, height = CANVAS_SIZE

        with pygame.PixelArray(self.surface) as pixels:
            while q:
                x, y = q.popleft()
                
                # Skip invalid coordinates
                if x < 0 or x >= width or y < 0 or y >= height:
                    continue
                
                # Skip non-matching colors
                if pixels[x, y] != old_rgb:
                    continue

                # Find west and east boundaries
                west = east = x
                while west >= 0 and pixels[west, y] == old_rgb:
                    west -= 1
                while east < width and pixels[east, y] == old_rgb:
                    east += 1

                # Paint the scanline
                pixels[west+1:east, y] = new_rgb

                # Queue adjacent rows
                for dx in range(west + 1, east):
                    if y > 0 and pixels[dx, y-1] == old_rgb:
                        q.append((dx, y-1))
                    if y < height-1 and pixels[dx, y+1] == old_rgb:
                        q.append((dx, y+1))

        self.save_state()