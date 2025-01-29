import pygame
import random
import math
from game_manager import GameManager

def main():
    game_manager = GameManager()
    game_manager.main_menu()
    game_manager.game_initialize()

    running = True
    is_shooting = False
    shooting_timer = 0
    shoot_timer = 0
    speed_boost_active = False
    speed_boost_timer = 0
    rate_boost_active = False
    rate_boost_timer = 0
    fullscreen = False

    while running:
        game_manager.screen.fill(game_manager.black)
        game_manager.screen.blit(game_manager.background_img, (0, game_manager.background_y))
        game_manager.screen.blit(game_manager.background_img, (0, game_manager.background_y + game_manager.SCREEN_HEIGHT))
        game_manager.background_y -= game_manager.background_speed
        if game_manager.background_y <= -game_manager.SCREEN_HEIGHT:
            game_manager.background_y = 0

        score_text = game_manager.font.render('Score: ' + str(game_manager.score), True, game_manager.green)
        lives_text = game_manager.font.render('Lives: ' + str(game_manager.lives), True, game_manager.green)
        game_manager.screen.blit(score_text, (10, 10))
        game_manager.screen.blit(lives_text, (game_manager.SCREEN_WIDTH - 150, 10))

        elapsed_time = pygame.time.get_ticks() - game_manager.start_time
        if elapsed_time >= 3 * 60 * 1000:
            game_manager.enemies.clear()

        current_time = pygame.time.get_ticks()
        if current_time - game_manager.rate_powerup_spawn_time >= 10000:
            game_manager.rate_pickup = [random.randint(0, game_manager.SCREEN_WIDTH - game_manager.pickup_size), random.randint(0, 200)]
            game_manager.rate_powerup_spawn_time = current_time

        if current_time - game_manager.speed_powerup_spawn_time >= 15000:
            game_manager.speed_pickup = [random.randint(0, game_manager.SCREEN_WIDTH - game_manager.pickup_size), random.randint(0, 200)]
            game_manager.speed_powerup_spawn_time = current_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and shoot_timer <= 0:
                    game_manager.bullets.append([game_manager.player_x + game_manager.player_width / 2 - game_manager.bullet_width / 2, game_manager.player_y])
                    game_manager.shoot_sound.play()
                    is_shooting = True
                    shooting_timer = 10
                    shoot_timer = game_manager.shoot_cooldown
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_p:
                    game_manager.pause_menu()
                if event.key == pygame.K_f:
                    fullscreen = not fullscreen
                    if fullscreen:
                        game_manager.screen = pygame.display.set_mode((game_manager.SCREEN_WIDTH, game_manager.SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        game_manager.screen = pygame.display.set_mode((game_manager.SCREEN_WIDTH, game_manager.SCREEN_HEIGHT))

        if shoot_timer > 0:
            shoot_timer -= 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and game_manager.player_x > 0:
            game_manager.player_x -= game_manager.player_speed
        if keys[pygame.K_RIGHT] and game_manager.player_x < game_manager.SCREEN_WIDTH - game_manager.player_width:
            game_manager.player_x += game_manager.player_speed

        if is_shooting:
            game_manager.screen.blit(game_manager.player_shooting_img, (game_manager.player_x, game_manager.player_y))
            shooting_timer -= 1
            if shooting_timer <= 0:
                is_shooting = False
        else:
            game_manager.screen.blit(game_manager.player_idle_img, (game_manager.player_x, game_manager.player_y))

        for bullet in game_manager.bullets[:]:
            bullet[1] -= game_manager.bullet_speed
            if bullet[1] < 0:
                game_manager.bullets.remove(bullet)
            game_manager.screen.blit(game_manager.bullet_img, (bullet[0], bullet[1]))

        enemies_to_remove = []
        for enemy in game_manager.enemies:
            enemy[1] += game_manager.enemy_speed
            game_manager.screen.blit(game_manager.enemy_img, (enemy[0], enemy[1]))
            for bullet in game_manager.bullets[:]:
                if enemy[0] < bullet[0] < enemy[0] + game_manager.enemy_size and enemy[1] < bullet[1] < enemy[1] + game_manager.enemy_size:
                    game_manager.bullets.remove(bullet)
                    enemies_to_remove.append(enemy)
                    game_manager.score += 10
                    game_manager.spawn_enemy()
                    game_manager.collision_sound.stop()
                    game_manager.collision_sound.play()
                    game_manager.particle_system.emit(enemy[0] + game_manager.enemy_size // 2, enemy[1] + game_manager.enemy_size // 2)
                    break

            if enemy[1] + game_manager.enemy_size > game_manager.SCREEN_HEIGHT:
                game_manager.lives -= 1
                enemies_to_remove.append(enemy)

        for enemy in enemies_to_remove:
            if enemy in game_manager.enemies:
                game_manager.enemies.remove(enemy)

        game_manager.life_pickup[1] += game_manager.enemy_speed
        game_manager.screen.blit(game_manager.life_pickup_img, (game_manager.life_pickup[0], game_manager.life_pickup[1]))

        if game_manager.player_x < game_manager.life_pickup[0] + game_manager.pickup_size and game_manager.player_x + game_manager.player_width > game_manager.life_pickup[0] and \
                game_manager.player_y < game_manager.life_pickup[1] + game_manager.pickup_size and game_manager.player_y + game_manager.player_height > game_manager.life_pickup[1]:
            game_manager.lives += 1
            game_manager.life_pickup = [random.randint(0, game_manager.SCREEN_WIDTH - game_manager.pickup_size), random.randint(0, 200)]
            game_manager.pickup_sound.play()

        game_manager.speed_pickup[1] += game_manager.enemy_speed
        game_manager.screen.blit(game_manager.speed_pickup_img, (game_manager.speed_pickup[0], game_manager.speed_pickup[1]))

        if game_manager.player_x < game_manager.speed_pickup[0] + game_manager.pickup_size and game_manager.player_x + game_manager.player_width > game_manager.speed_pickup[0] and \
                game_manager.player_y < game_manager.speed_pickup[1] + game_manager.pickup_size and game_manager.player_y + game_manager.player_height > game_manager.speed_pickup[1]:
            game_manager.player_speed *= 1.25
            game_manager.speed_pickup = [random.randint(0, game_manager.SCREEN_WIDTH - game_manager.pickup_size), random.randint(0, 200)]
            game_manager.speed_sound.play()
            speed_boost_active = True
            speed_boost_timer = 300

        game_manager.rate_pickup[1] += game_manager.enemy_speed
        game_manager.screen.blit(game_manager.rate_pickup_img, (game_manager.rate_pickup[0], game_manager.rate_pickup[1]))

        if game_manager.player_x < game_manager.rate_pickup[0] + game_manager.pickup_size and game_manager.player_x + game_manager.player_width > game_manager.rate_pickup[0] and \
                game_manager.player_y < game_manager.rate_pickup[1] + game_manager.pickup_size and game_manager.player_y + game_manager.player_height > game_manager.rate_pickup[1]:
            game_manager.shoot_cooldown = game_manager.default_shoot_cooldown // 2
            game_manager.rate_pickup = [random.randint(0, game_manager.SCREEN_WIDTH - game_manager.pickup_size), random.randint(0, 200)]
            game_manager.rate_sound.play()
            rate_boost_active = True
            rate_boost_timer = 300

        if speed_boost_active:
            speed_boost_timer -= 1
            if speed_boost_timer <= 0:
                game_manager.player_speed /= 1.25
                speed_boost_active = False

        if rate_boost_active:
            rate_boost_timer -= 1
            if rate_boost_timer <= 0:
                game_manager.shoot_cooldown = game_manager.default_shoot_cooldown
                rate_boost_active = False

        if speed_boost_active:
            game_manager.screen.blit(game_manager.speed_pickup_img, (10, 50))
        if rate_boost_active:
            game_manager.screen.blit(game_manager.rate_pickup_img, (10, 90))

        if game_manager.score >= 300 and not game_manager.boss_appeared:
            game_manager.boss_appeared = True

        if game_manager.boss_appeared:
            game_manager.boss_angle += game_manager.boss_speed
            game_manager.boss_x = game_manager.SCREEN_WIDTH // 2 + int(100 * math.cos(math.radians(game_manager.boss_angle))) - game_manager.boss_size // 2
            game_manager.boss_y = game_manager.SCREEN_HEIGHT // 2 + int(100 * math.sin(math.radians(game_manager.boss_angle))) - game_manager.boss_size // 2
            game_manager.screen.blit(game_manager.boss_img, (game_manager.boss_x, game_manager.boss_y))

            game_manager.boss_shoot_timer -= 1
            if game_manager.boss_shoot_timer <= 0:
                game_manager.boss_bullets.append([game_manager.boss_x + game_manager.boss_size / 2 - game_manager.bullet_width / 2, game_manager.boss_y + game_manager.boss_size])
                game_manager.boss_shoot_timer = 50

            for boss_bullet in game_manager.boss_bullets[:]:
                boss_bullet[1] += game_manager.bullet_speed
                if boss_bullet[1] > game_manager.SCREEN_HEIGHT:
                    game_manager.boss_bullets.remove(boss_bullet)
                game_manager.screen.blit(game_manager.rotated_bullet_img, (boss_bullet[0], boss_bullet[1]))

            for boss_bullet in game_manager.boss_bullets[:]:
                if game_manager.player_x < boss_bullet[0] + game_manager.bullet_width and game_manager.player_x + game_manager.player_width > boss_bullet[0] and \
                        game_manager.player_y < boss_bullet[1] + game_manager.bullet_height and game_manager.player_y + game_manager.player_height > boss_bullet[1]:
                    game_manager.lives -= 1
                    game_manager.boss_bullets.remove(boss_bullet)
                    game_manager.lose_life_sound.play()

            for bullet in game_manager.bullets[:]:
                if game_manager.boss_x < bullet[0] < game_manager.boss_x + game_manager.boss_size and game_manager.boss_y < bullet[1] < game_manager.boss_y + game_manager.boss_size:
                    game_manager.bullets.remove(bullet)
                    game_manager.boss_health -= 1
                    game_manager.collision_sound.play()
                    game_manager.particle_system.emit(game_manager.boss_x + game_manager.boss_size // 2, game_manager.boss_y + game_manager.boss_size // 2, size=10)
                    if game_manager.boss_health <= 0:
                        for _ in range(50):
                            game_manager.particle_system.emit(game_manager.boss_x + game_manager.boss_size // 2, game_manager.boss_y + game_manager.boss_size // 2, size=20)
                        game_manager.show_warp_speed_message("Warp speed activated!")  # Show warp speed message
                        game_manager.start_warp_speed_level()  # Start next level
                        game_manager.game_initialize()

        if game_manager.boss_appeared:
            for i in range(game_manager.boss_health):
                game_manager.screen.blit(pygame.transform.scale(game_manager.boss_img, (game_manager.boss_size // 5, game_manager.boss_size // 5)), (game_manager.SCREEN_WIDTH // 2 + (i % 10) * 12 - 60, 10 + (i // 10) * 12))

        if not game_manager.enemies and not game_manager.boss_appeared:
            game_manager.show_end_game_message("You Win!")
            game_manager.game_initialize()

        if game_manager.lives <= 0:
            game_manager.enter_initials()
            game_manager.show_leaderboard(after_initials=True)
            game_manager.show_end_game_message("Game Over")
            game_manager.game_initialize()
        elif game_manager.lives < 3:
            game_manager.lose_life_sound.play()

        game_manager.particle_system.update()

        pygame.display.flip()
        game_manager.clock.tick(44)

if __name__ == "__main__":
    main()
