import os
import pygame
import random
import json
import math

class GameManager:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Screen dimensions
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 600
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # Directorio de recursos
        self.asset_dir = os.path.join(os.path.dirname(__file__), 'assets')

        # Color variables
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)

        # Load images
        self.player_idle_img = pygame.image.load(os.path.join(self.asset_dir, 'player_1.png'))
        self.player_shooting_img = pygame.image.load(os.path.join(self.asset_dir, 'player_5.png'))
        self.enemy_img = pygame.image.load(os.path.join(self.asset_dir, 'enemy_1.png'))
        self.enemy_hit_img = pygame.image.load(os.path.join(self.asset_dir, 'enemy_3.png'))
        self.bullet_img = pygame.image.load(os.path.join(self.asset_dir, 'Bullet.gif'))
        self.rotated_bullet_img = pygame.transform.rotate(self.bullet_img, 180)
        self.life_pickup_img = pygame.image.load(os.path.join(self.asset_dir, 'Life.png'))
        self.speed_pickup_img = pygame.image.load(os.path.join(self.asset_dir, 'speed.png'))
        self.rate_pickup_img = pygame.image.load(os.path.join(self.asset_dir, 'rate.png'))
        self.background_img = pygame.image.load(os.path.join(self.asset_dir, 'background_4.png'))
        self.boss_img = pygame.image.load(os.path.join(self.asset_dir, 'boss.png'))

        # Load music
        pygame.mixer.music.load(os.path.join(self.asset_dir, 'backingtrack.mp3'))
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        # Load sounds
        self.shoot_sound = pygame.mixer.Sound(os.path.join(self.asset_dir, 'shoot.wav'))
        self.collision_sound = pygame.mixer.Sound(os.path.join(self.asset_dir, 'collision.wav'))
        self.pickup_sound = pygame.mixer.Sound(os.path.join(self.asset_dir, 'pickup.wav'))
        self.lose_life_sound = pygame.mixer.Sound(os.path.join(self.asset_dir, 'loselife.wav'))
        self.speed_sound = pygame.mixer.Sound(os.path.join(self.asset_dir, 'speed.mp3'))
        self.rate_sound = pygame.mixer.Sound(os.path.join(self.asset_dir, 'rate.mp3'))

        # Font for score, lives, and end game messages
        self.font = pygame.font.SysFont(None, 36)
        self.end_game_font = pygame.font.SysFont("comicsansms", 72)
        self.menu_font = pygame.font.SysFont("comicsansms", 48)

        # Background scrolling variables
        self.background_y = 0
        self.background_speed = 2

        # Player properties
        self.player_width = 60
        self.player_height = 25
        self.player_speed = 15
        self.player_x = self.SCREEN_WIDTH / 2 - self.player_width / 2
        self.player_y = self.SCREEN_HEIGHT - self.player_height - 10

        # Bullet properties
        self.bullet_width = 10
        self.bullet_height = 20
        self.bullet_speed = 10

        # Enemy properties
        self.enemy_size = 50
        self.enemy_speed = 2

        # Life pickup properties
        self.pickup_size = 20

        # Boss enemy properties
        self.boss_size = 100
        self.boss_speed = 3
        self.boss_appeared = False
        self.boss_x = 0
        self.boss_y = 0
        self.boss_angle = 0
        self.boss_bullets = []
        self.boss_shoot_timer = 0
        self.boss_health = 20

        # Initialize the particle system for collisions
        self.particle_system = ParticleSystem(self.screen)

        # Clock for controlling the frame rate
        self.clock = pygame.time.Clock()

        # Game speed multiplier
        self.game_speed_multiplier = 1.0  # Change this value to adjust the overall game speed

    # Initializes or resets the game elements
    def game_initialize(self):
        self.score = 0
        self.lives = 5
        self.player_speed = 15
        self.default_shoot_cooldown = 5
        self.shoot_cooldown = self.default_shoot_cooldown
        self.player_x = self.SCREEN_WIDTH / 2 - self.player_width / 2
        self.bullets = []
        self.enemies = [[random.randint(0, self.SCREEN_WIDTH - self.enemy_size), random.randint(0, 200)] for _ in range(10)]
        self.life_pickup = [random.randint(0, self.SCREEN_WIDTH - self.pickup_size), random.randint(0, 200)]
        self.speed_pickup = [random.randint(0, self.SCREEN_WIDTH - self.pickup_size), random.randint(0, 200)]
        self.rate_pickup = [random.randint(0, self.SCREEN_WIDTH - self.pickup_size), random.randint(0, 200)]
        self.rate_powerup_spawn_time = pygame.time.get_ticks()
        self.speed_powerup_spawn_time = pygame.time.get_ticks()
        self.start_time = pygame.time.get_ticks()

        self.boss_appeared = False
        self.boss_x = self.SCREEN_WIDTH // 2 - self.boss_size // 2
        self.boss_y = -self.boss_size
        self.boss_angle = 0
        self.boss_bullets = []
        self.boss_shoot_timer = 0
        self.boss_health = 20

    # Displays the end game screen (Game Over or You Win) and waits for player input
    def show_end_game_message(self, message):
        self.screen.fill(self.black)
        end_game_text = self.end_game_font.render(message, True, self.red)
        score_text = self.font.render(f"Final Score: {self.score}", True, self.white)
        restart_text = self.font.render("Press C to continue or Esc to quit", True, self.green)
        self.screen.blit(end_game_text, (self.SCREEN_WIDTH // 2 - end_game_text.get_width() // 2, self.SCREEN_HEIGHT // 3))
        self.screen.blit(score_text, (self.SCREEN_WIDTH // 2 - score_text.get_width() // 2, self.SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, self.SCREEN_HEIGHT // 2 + 50))
        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        self.game_initialize()  # Continue the game with current lives and score
                        return
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

    # Spawn a new enemy
    def spawn_enemy(self):
        self.enemies.append([random.randint(0, self.SCREEN_WIDTH - self.enemy_size), random.randint(0, 200)])

    def main_menu(self):
        menu_running = True
        while menu_running:
            self.screen.fill(self.black)
            title_text = self.menu_font.render("Most Wanted UFO", True, self.white)
            start_text = self.font.render("Start Game", True, self.green)
            exit_text = self.font.render("Exit", True, self.red)
            fullscreen_text = self.font.render("Full Screen", True, self.green)

            self.screen.blit(title_text, (self.SCREEN_WIDTH // 2 - title_text.get_width() // 2, self.SCREEN_HEIGHT // 3))
            self.screen.blit(start_text, (self.SCREEN_WIDTH // 2 - start_text.get_width() // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(fullscreen_text, (self.SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2, self.SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(exit_text, (self.SCREEN_WIDTH // 2 - exit_text.get_width() // 2, self.SCREEN_HEIGHT // 2 + 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu_running = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if self.SCREEN_WIDTH // 2 - start_text.get_width() // 2 < mouse_x < self.SCREEN_WIDTH // 2 + start_text.get_width() // 2 and \
                            self.SCREEN_HEIGHT // 2 < mouse_y < self.SCREEN_HEIGHT // 2 + start_text.get_height():
                        menu_running = False
                    if self.SCREEN_WIDTH // 2 - exit_text.get_width() // 2 < mouse_x < self.SCREEN_WIDTH // 2 + exit_text.get_width() // 2 and \
                            self.SCREEN_HEIGHT // 2 + 100 < mouse_y < self.SCREEN_HEIGHT // 2 + 100 + exit_text.get_height():
                        pygame.quit()
                        sys.exit()
                    if self.SCREEN_WIDTH // 2 - fullscreen_text.get_width() // 2 < mouse_x < self.SCREEN_WIDTH // 2 + fullscreen_text.get_width() // 2 and \
                            self.SCREEN_HEIGHT // 2 + 50 < mouse_y < self.SCREEN_HEIGHT // 2 + 50 + fullscreen_text.get_height():
                        pygame.display.toggle_fullscreen()

    def pause_menu(self):
        paused = True
        while paused:
            self.screen.fill(self.black)
            pause_text = self.menu_font.render("Paused", True, self.white)
            resume_text = self.font.render("Press R to Resume", True, self.green)
            restart_text = self.font.render("Press Enter to Restart", True, self.green)
            quit_text = self.font.render("Press Esc to Quit", True, self.red)

            self.screen.blit(pause_text, (self.SCREEN_WIDTH // 2 - pause_text.get_width() // 2, self.SCREEN_HEIGHT // 3))
            self.screen.blit(resume_text, (self.SCREEN_WIDTH // 2 - resume_text.get_width() // 2, self.SCREEN_HEIGHT // 2))
            self.screen.blit(restart_text, (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, self.SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(quit_text, (self.SCREEN_WIDTH // 2 - quit_text.get_width() // 2, self.SCREEN_HEIGHT // 2 + 100))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        paused = False
                    if event.key == pygame.K_RETURN:
                        self.game_initialize()
                        paused = False
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def enter_initials(self):
        initials = ""
        enter_initials_running = True
        while enter_initials_running:
            self.screen.fill(self.black)
            enter_initials_text = self.menu_font.render("Enter Initials:", True, self.white)
            initials_text = self.menu_font.render(initials, True, self.green)
            self.screen.blit(enter_initials_text, (self.SCREEN_WIDTH // 2 - enter_initials_text.get_width() // 2, self.SCREEN_HEIGHT // 3))
            self.screen.blit(initials_text, (self.SCREEN_WIDTH // 2 - initials_text.get_width() // 2, self.SCREEN_HEIGHT // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(initials) == 3:
                        enter_initials_running = False
                    elif event.key == pygame.K_BACKSPACE:
                        initials = initials[:-1]
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()

        self.update_leaderboard(initials, self.score)
        self.show_leaderboard(after_initials=True)

    def update_leaderboard(self, initials, score):
        leaderboard_file = "leaderboard.json"
        try:
            with open(leaderboard_file, "r") as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = []

        leaderboard.append({"initials": initials, "score": score})
        leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:10]

        with open(leaderboard_file, "w") as file:
            json.dump(leaderboard, file)

    def show_leaderboard(self, after_initials=False):
        leaderboard_file = "leaderboard.json"
        try:
            with open(leaderboard_file, "r") as file:
                leaderboard = json.load(file)
        except FileNotFoundError:
            leaderboard = []

        self.screen.fill(self.black)
        title_text = self.menu_font.render("Leaderboard", True, self.white)
        self.screen.blit(title_text, (self.SCREEN_WIDTH // 2 - title_text.get_width() // 2, self.SCREEN_HEIGHT // 16))
        for i, entry in enumerate(leaderboard):
            entry_text = self.font.render(f"{i + 1}. {entry['initials']} - {entry['score']}", True, self.green)
            self.screen.blit(entry_text, (self.SCREEN_WIDTH // 2 - entry_text.get_width() // 2, self.SCREEN_HEIGHT // 10 + 60 + i * 30))

        pygame.display.flip()
        pygame.time.wait(5000)

    def update(self):
        # Update background position
        self.background_y -= self.background_speed * self.game_speed_multiplier
        if self.background_y <= -self.SCREEN_HEIGHT:
            self.background_y = 0

        # Update bullets
        for bullet in self.bullets[:]:
            bullet[1] -= self.bullet_speed * self.game_speed_multiplier
            if bullet[1] < 0:
                self.bullets.remove(bullet)

        # Update enemies
        for enemy in self.enemies[:]:
            enemy[1] += self.enemy_speed * self.game_speed_multiplier
            if enemy[1] + self.enemy_size > self.SCREEN_HEIGHT:
                self.enemies.remove(enemy)
                self.lives -= 1

        # Update boss position and bullets if boss appeared
        if self.boss_appeared:
            self.boss_angle += self.boss_speed * self.game_speed_multiplier
            self.boss_x = self.SCREEN_WIDTH // 2 + int(100 * math.cos(math.radians(self.boss_angle))) - self.boss_size // 2
            self.boss_y = self.SCREEN_HEIGHT // 2 + int(100 * math.sin(math.radians(self.boss_angle))) - self.boss_size // 2

            # Update boss bullets
            for boss_bullet in self.boss_bullets[:]:
                boss_bullet[1] += self.bullet_speed * self.game_speed_multiplier
                if boss_bullet[1] > self.SCREEN_HEIGHT:
                    self.boss_bullets.remove(boss_bullet)

        # Other update code...

    def draw(self):
        self.screen.fill(self.black)
        self.screen.blit(self.background_img, (0, self.background_y))
        self.screen.blit(self.background_img, (0, self.background_y + self.SCREEN_HEIGHT))

        # Draw other game elements...

        pygame.display.flip()

class ParticleSystem:
    def __init__(self, screen):
        self.screen = screen
        self.particles = []

    def emit(self, x, y, size=5, color=(255, 0, 0)):
        self.particles.append([x, y, size, color])

    def update(self):
        for particle in self.particles[:]:
            particle[2] -= 0.2
            if particle[2] <= 0:
                self.particles.remove(particle)
            else:
                pygame.draw.circle(self.screen, particle[3], (int(particle[0]), int(particle[1])), int(particle[2]))

# Example usage:
if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.game_initialize()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game_manager.update()
        game_manager.draw()
        game_manager.clock.tick(60)

    pygame.quit()
