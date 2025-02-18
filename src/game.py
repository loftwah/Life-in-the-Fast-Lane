import pygame
import pygame_menu
from src.player import Player
from src.ui.menu import MainMenu
from game_config import FPS
from src.locations import Location

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = None
        self.turn = 0
        self.menu = MainMenu(self)
        self.locations = []
        self.setup_locations()
        
    def setup_locations(self):
        """Create and set up game locations"""
        # Housing
        apartment = Location("Cramped Quarters", "housing", 50, 100)
        apartment.add_action("Rest", 0, {"energy": 3, "happiness": 1})
        apartment.add_action("Sleep", 0, {"energy": 5, "health": 1})
        
        # Work
        burger_joint = Location("Monolith Burgers", "work", 300, 100)
        burger_joint.add_action("Work Shift", 2, {"money": 50, "happiness": -1})
        burger_joint.add_action("Overtime", 3, {"money": 80, "happiness": -2})
        
        # Education
        university = Location("Metro University", "education", 550, 100)
        university.add_action("Study", 2, {"education": 1, "energy": -1})
        university.add_action("Take Class", 3, {"education": 2, "money": -100})
        
        self.locations.extend([apartment, burger_joint, university])
        
    def start_game(self, player_data):
        """Start a new game with the given player data"""
        self.player = Player(player_data["name"], player_data["stats"])
        self.turn = 1
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            if self.player is None:
                self.menu.show()
            else:
                self.update()
                self.render()
                
            pygame.display.flip()
            self.clock.tick(FPS)
    
    def handle_events(self):
        """Handle pygame events"""
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE and self.player:
                    # TODO: Show pause menu
                    pass
        
        # Update location hover states
        for loc in self.locations:
            loc.handle_mouse(mouse_pos)
    
    def handle_click(self, pos):
        """Handle mouse clicks on locations"""
        if not self.player:
            return
            
        for loc in self.locations:
            if loc.handle_mouse(pos):
                self.show_location_actions(loc)
                break
    
    def show_location_actions(self, location):
        """Show available actions for the selected location"""
        # Create a temporary menu for location actions
        action_menu = pygame_menu.Menu(
            location.name,
            400, 300,
            theme=pygame_menu.themes.THEME_DARK
        )
        
        for action in location.actions:
            action_menu.add.button(
                f"{action['name']} (Energy: {action['energy_cost']})",
                lambda a=action: self.perform_action(location, a)
            )
        
        action_menu.add.button("Close", action_menu.disable)
        action_menu.mainloop(self.screen)
    
    def perform_action(self, location, action):
        """Perform the selected action if player has enough energy"""
        if self.player.energy >= action["energy_cost"]:
            self.player.energy -= action["energy_cost"]
            
            # Apply action effects
            for stat, value in action["effects"].items():
                if hasattr(self.player, stat):
                    current = getattr(self.player, stat)
                    setattr(self.player, stat, current + value)
    
    def update(self):
        """Update game state"""
        if self.player:
            self.player.update()
    
    def render(self):
        """Render the game"""
        self.screen.fill((200, 200, 200))  # Background
        
        # Render locations
        for location in self.locations:
            location.render(self.screen)
            
        # Render player stats
        if self.player:
            self.player.render(self.screen) 