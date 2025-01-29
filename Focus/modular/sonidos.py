import pygame

# Inicializar Pygame
pygame.mixer.init()

def cargar_sonido(ruta):
    try:
        return pygame.mixer.Sound(ruta)
    except pygame.error as e:
        print(f"Error al cargar el sonido {ruta}: {e}")
        return None
