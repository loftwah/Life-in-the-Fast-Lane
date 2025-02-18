import pygame
from game_config import WHITE

class Player:
    def __init__(self, name, stats):
        self.name = name
        self.money = stats.get("money", 100)
        self.happiness = stats.get("happiness", 50)
        self.education = stats.get("education", 0)
        self.health = stats.get("health", 75)
        self.energy = stats.get("energy", 5)
        self.max_energy = self.energy
        self.location = None
        
    def update(self):
        """Update player state"""
        # Simulate basic needs decay
        self.energy = max(0, self.energy - 0.1)
        if self.energy < 2:
            self.health = max(0, self.health - 0.5)
            self.happiness = max(0, self.happiness - 1)
    
    def render(self, screen):
        """Render player stats"""
        font = pygame.font.SysFont(None, 24)
        stats = [
            f"Name: {self.name}",
            f"Money: ${self.money}",
            f"Happiness: {int(self.happiness)}",
            f"Education: {int(self.education)}",
            f"Health: {int(self.health)}",
            f"Energy: {int(self.energy)}/{self.max_energy}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, WHITE)
            screen.blit(text, (10, 10 + i * 30)) 