import pygame

class ParticleSystem:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []

    def emit(self, x, y, size=5, color=(255, 0, 0)):
        self.particles.append([x, y, size, color])

    def update(self):
        for particle in self.particles[:]:
            particle[2] -= 0.2  # Reduce the size of particles
            if particle[2] <= 0:
                self.particles.remove(particle)
            else:
                pygame.draw.circle(self.screen, particle[3], (int(particle[0]), int(particle[1])), int(particle[2]))
