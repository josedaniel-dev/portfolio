import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Color variables
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Fonts
pygame.init()
FONT = pygame.font.SysFont(None, 36)
END_GAME_FONT = pygame.font.SysFont("comicsansms", 72)
MENU_FONT = pygame.font.SysFont("comicsansms", 48)

# Other constants
PLAYER_Y = SCREEN_HEIGHT - 35
BOSS_SIZE = 100
