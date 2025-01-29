import pygame
import random
from config import *

class Player:
    def __init__(self):
        self.image = PLAYER_IDLE_IMG
        self.shooting_image = PLAYER_SHOOTING_IMG
        self.rect = self.image.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10))
        self.speed = 15
        self.bullets = []
        self.shooting = False
        self.shooting_timer = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        self.bullets.append(Bullet(self.rect.centerx, self.rect.top))
        SHOOT_SOUND.play()
        self.shooting = True
        self.shooting_timer = 10

    def draw(self, screen):
        if self.shooting:
            screen.blit(self.shooting_image, self.rect)
            self.shooting_timer -= 1
            if self.shooting_timer <= 0:
                self.shooting = False
        else:
            screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y):
        self.image = BULLET_IMG
        self.rect = self.image.get_rect(midbottom=(x, y))
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self):
        self.image = ENEMY_IMG
        self.rect = self.image.get_rect(midtop=(random.randint(0, SCREEN_WIDTH - self.image.get_width()), random.randint(0, 200)))
        self.speed = 2

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Boss:
    def __init__(self):
        self.image = BOSS_IMG
        self.rect = self.image.get_rect(midtop=(SCREEN_WIDTH / 2, -100))
        self.speed = 3
        self.angle = 0
        self.bullets = []
        self.shoot_timer = 0
        self.health = 20

    def update(self):
        self.angle += self.speed
        self.rect.x = SCREEN_WIDTH // 2 + int(100 * math.cos(math.radians(self.angle))) - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT // 2 + int(100 * math.sin(math.radians(self.angle))) - self.rect.height // 2

    def shoot(self):
        self.bullets.append(Bullet(self.rect.centerx, self.rect.bottom))
        self.shoot_timer = 50

    def draw(self, screen):
        screen.blit(self.image, self.rect)
