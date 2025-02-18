import pygame
import sys
from src.game import Game
from game_config import SCREEN_WIDTH, SCREEN_HEIGHT, TITLE

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    
    game = Game(screen)
    game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 