import pygame
from game_config import WHITE, BLACK, GRAY

class Location:
    def __init__(self, name, type, x, y, width=200, height=100):
        self.name = name
        self.type = type
        self.rect = pygame.Rect(x, y, width, height)
        self.actions = []
        self.hover = False
        
    def add_action(self, name, energy_cost, effects):
        """Add an available action at this location"""
        self.actions.append({
            "name": name,
            "energy_cost": energy_cost,
            "effects": effects
        })
        
    def render(self, screen):
        """Render the location as a clickable area"""
        color = GRAY if self.hover else BLACK
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)  # Border
        
        # Render location name
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.name, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        
    def handle_mouse(self, pos):
        """Update hover state and handle clicks"""
        self.hover = self.rect.collidepoint(pos)
        return self.hover 