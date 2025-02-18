import pygame_menu
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.player_name = "Player"
        self.menu = pygame_menu.Menu(
            TITLE,
            SCREEN_WIDTH,
            SCREEN_HEIGHT,
            theme=pygame_menu.themes.THEME_DARK
        )
        self.setup_menu()
        
    def setup_menu(self):
        """Set up the main menu items"""
        self.menu.add.text_input("Name: ", default=self.player_name, onchange=self.set_player_name)
        self.menu.add.button("New Game", self.start_game)
        self.menu.add.button("Quit", pygame_menu.events.EXIT)
    
    def set_player_name(self, value):
        """Set the player name from input"""
        self.player_name = value
    
    def start_game(self):
        """Start a new game with current settings"""
        # Default starting stats
        stats = {
            "money": 100,
            "happiness": 50,
            "education": 0,
            "health": 75,
            "energy": 5
        }
        self.game.start_game({"name": self.player_name, "stats": stats})
        self.menu.disable()
    
    def show(self):
        """Display the menu"""
        self.menu.mainloop(self.game.screen) 