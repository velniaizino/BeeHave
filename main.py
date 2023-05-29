import random
import pygame
from pygame.locals import *
import sys
from sqlalchemy.orm import sessionmaker
from highscore import engine, Score
from player import Player
from obstacle import Obstacle
from life import Life
from button import Button
from heart import Heart

Session = sessionmaker(bind=engine)
session = Session()


def check_score(recent_score, player_num, best):
    player_data = session.query(Score).filter_by(player_id=player_num).first()
    if player_data is not None:
        player_data.best = best
        player_data.last = recent_score
        session.commit()

    if player_data is None:
        player_data = Score(player_num, 0, recent_score)
        session.add(player_data)
        session.commit()


def get_best_score(player_num):
    player_data = session.query(Score).filter_by(player_id=player_num).first()
    best = 0
    if player_data is not None:
        best = player_data.best
    session.commit()
    return best


def get_last_score(player_num):
    player_data = session.query(Score).filter_by(player_id=player_num).first()
    last = 0
    if player_data is not None:
        last = player_data.last
    session.commit()
    return last


def check_collisions(player_coll, obstacles):
    player_coll.rect.topleft = (player_coll.rect.x, player_coll.rect.y)
    for obstacle_coll in obstacles:
        obstacle_coll.rect.topleft = (obstacle_coll.rect.x, obstacle_coll.rect.y)
        if pygame.sprite.collide_rect(player_coll, obstacle_coll):
            obstacle_coll.kill()
            obstacles.remove(obstacle_coll)
            player_coll.lives -= 1


def check_heart_collisions(player_coll, hearts):
    player_coll.rect.topleft = (player_coll.rect.x, player_coll.rect.y)
    for heart in hearts:
        heart.rect.topleft = (heart.rect.x, heart.rect.y)
        if pygame.sprite.collide_rect(player_coll, heart):
            heart.kill()
            hearts.remove(heart)
            if 0 < player_coll.lives < 3:
                player_coll.lives += 1


def check_lives(lives_list, player_lives):
    is_alive = True
    if int(player_lives.lives) >= 3:
        for life in lives_list:
            life.get_life()
    if int(player_lives.lives) == 2:
        lives_list[0].loose_life()
        lives_list[1].get_life()
        lives_list[2].get_life()
    if int(player_lives.lives) == 1:
        lives_list[0].loose_life()
        lives_list[1].loose_life()
        lives_list[2].get_life()
    if int(player_lives.lives) == 0:
        lives_list[0].loose_life()
        lives_list[1].loose_life()
        lives_list[2].loose_life()
        is_alive = False
    return is_alive


def reduce_sapwn_pause(current_score, current_spawn_pause):
    if current_score >= 20:
        current_spawn_pause -= current_score / 50000
    if current_spawn_pause <= 200:
        current_spawn_pause = 200
    return current_spawn_pause


def main():
    # colors
    yellow = (224, 189, 16)
    blue = (115, 147, 179)
    purple = (83, 5, 106)
    # screen dimensions
    screen_width = 480
    screen_height = 720
    # game icon
    icon = pygame.image.load('images/icon_32.ico')
    # game init params
    fps = 60
    game_paused = True

    # time
    last_spawn_time = pygame.time.get_ticks()
    last_heart_spawn = pygame.time.get_ticks()
    start_time = pygame.time.get_ticks()

    # player info
    player_id = "Vardas"
    player_pos_x = 240
    player_pos_y = 450
    player = Player(player_pos_x, player_pos_y)
    player_velocity = 7

    # game init
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("BeeHave")
    pygame.display.set_icon(icon)
    timer = pygame.time.Clock()
    # background
    bg_source = pygame.image.load('images/background.png')
    bg_y = bg_source.get_height()
    bg = pygame.transform.scale(bg_source, (bg_source.get_width() * 1, bg_source.get_height()) * 1)
    y = 0
    # fonts
    font = pygame.font.Font("fonts/PixelFont.ttf", 15)
    name_font = pygame.font.Font("fonts/PixelFont.ttf", 30)

    # UI
    lives_list = [
        Life(screen_width - 40, 20),
        Life(screen_width - 70, 20),
        Life(screen_width - 100, 20),
    ]
    play_button = Button(130, 300, pygame.image.load("images/play_button.png"), 2)
    quit_button = Button(130, 400, pygame.image.load("images/quit_button.png"), 2)
    # UI Score
    last_score = get_last_score(player_id)
    best_score = get_best_score(player_id)
    score_per_second = 3

    # obstacles
    obstacles_list = []
    spawn_pause = 600
    # hearts
    heart_list = []
    heart_spawn_pause = 6000
    # main loop
    run = True
    while run:
        timer.tick(fps)
        screen.fill(blue)

        # check if exited
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # check if paused
        if game_paused:
            screen_center = screen_width / 2
            game_text = name_font.render("BeeHave", True, yellow)
            game_rect = game_text.get_rect(center=(screen_center, 150))
            screen.blit(game_text, game_rect)
            best_text = font.render(f"BEST SCORE: {best_score}", True, yellow)
            best_rect = best_text.get_rect(center=(screen_center, 220))
            screen.blit(best_text, best_rect)
            last_text = font.render(f"LAST SCORE: {last_score}", True, yellow)
            last_rect = last_text.get_rect(center=(screen_center, 250))
            screen.blit(last_text, last_rect)
            if play_button.draw(screen):
                game_paused = False
            if quit_button.draw(screen):
                pygame.quit()
                sys.exit()
        else:
            # time variables
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            # score
            score = int((elapsed_time / 1000) * score_per_second)

            # create obstacles with spawn pause
            if current_time - last_spawn_time >= int(spawn_pause):
                last_spawn_time = current_time
                current_obstacle = Obstacle(
                    random.randint(0, screen_width - 35),
                    -50,
                    velocity=random.uniform(3.0, 5.5),
                )
                obstacles_list.append(current_obstacle)

            if current_time - last_heart_spawn >= int(heart_spawn_pause):
                last_heart_spawn = current_time
                current_heart = Heart(
                    random.randint(0, screen_width - 35),
                    -50,
                    velocity=random.uniform(2, 3),
                )
                heart_list.append(current_heart)
            # check if right arrow or left arrow is pressed
            key_pressed_is = pygame.key.get_pressed()
            if key_pressed_is[K_LEFT]:
                player.rect.x -= player_velocity
                player.rect.clamp_ip((screen.get_rect()))
            if key_pressed_is[K_RIGHT]:
                player.rect.x += player_velocity
                player.rect.clamp_ip((screen.get_rect()))

            # draw screen loop
            screen.fill(purple)
            screen.blit(bg, (0, y))
            screen.blit(bg, (0, -bg_y + y))
            if y == bg_y:
                screen.blit(bg, (0, -bg_y + y))
                y = 0
            y += 1
            # draw and update player
            player.draw(screen)
            player.update()
            # obstacle loop
            for obstacle in obstacles_list:
                obstacle.update()
                obstacle.draw(screen)
                # check if obstacle is off-screen
                if obstacle.rect.y > obstacle.height:
                    obstacle.kill()
                    obstacles_list.remove(obstacle)
            for heart in heart_list:
                heart.update()
                heart.draw(screen)
                # check if obstacle is off-screen
                if heart.rect.y > heart.height:
                    heart.kill()
                    heart_list.remove(heart)
            # draw lives
            for life in lives_list:
                life.draw(screen)

            # activate methods
            check_collisions(player, obstacles_list)
            check_heart_collisions(player, heart_list)
            alive = check_lives(lives_list, player)

            # if player died, update score and pause game
            if not alive:
                last_score = score
                if last_score > best_score:
                    best_score = last_score
                check_score(last_score, player_id, best_score)
                game_paused = True
                main()

            # make game harder depending on score
            spawn_pause = reduce_sapwn_pause(score, spawn_pause)

            # score text
            score_text = font.render("SCORE: " + str(score), True, yellow)
            screen.blit(score_text, (10, 10))
        pygame.display.update()


pygame.quit()

if __name__ == "__main__":
    main()
