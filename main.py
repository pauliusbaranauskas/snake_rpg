import pygame
import sys

from random import randint
import json

import os


def end_game():
    pygame.quit()
    sys.exit()


def read_settings():
    file_path = os.path.realpath(__file__)
    sep = os.path.sep
    file_path = file_path.split(sep)
    file_path = file_path[:-1]
    file_path.append("snake settings.json")
    file_path = sep.join(file_path)
    with open(file_path) as f:
        settings = f.read()
        settings = json.loads(settings)

    framerate = settings["speed"]
    cell_size = settings["cell_size"]
    cell_number = settings["cell_number"]

    return framerate, cell_size, cell_number


def direction(event, cell_size, x_step, y_step):
    if event.key == pygame.K_DOWN:
        if y_step == -cell_size:
            x_step, y_step = -1, -1
        else:
            x_step, y_step = 0, cell_size
    elif event.key == pygame.K_LEFT:
        if x_step == cell_size:
            x_step, y_step =  -1, -1
        else:
            x_step, y_step = -cell_size, 0
    elif event.key == pygame.K_UP:
        if y_step == cell_size:
            x_step, y_step =  -1, -1
        else:
            x_step, y_step = 0, -cell_size
    elif event.key == pygame.K_RIGHT:
        if x_step == -cell_size:
            x_step, y_step =  -1, -1
        else:
            x_step, y_step = cell_size, 0

    return x_step, y_step


def play_game(screen, cell_size, cell_number, font):
        
    x_step = cell_size
    y_step = 0
    score = 0

    food = pygame.Rect(randint(0, cell_number-1)*cell_size, randint(0, cell_number-1)*cell_size, cell_size, cell_size)

    blocks = [pygame.Rect(0+cell_size, 0, cell_size, cell_size),pygame.Rect(0, 0, cell_size, cell_size)]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()

            elif event.type == pygame.KEYDOWN:
                x_step, y_step = direction(event, cell_size, x_step, y_step)
                if x_step == y_step:
                    return score

        screen.fill(pygame.Color("grey"))

        for i, block in enumerate(reversed(blocks)):
            if i == len(blocks)-1:
                block.move_ip(x_step, y_step)
                if pygame.Rect.colliderect(block, food):
                    food.update(randint(0, cell_number-1)*cell_size, randint(0, cell_number-1)*cell_size, cell_size, cell_size)

                    score += 1

                    while food.collidelist(blocks) > -1:
                        food.update(randint(0, cell_number - 1) * cell_size, randint(0, cell_number - 1) * cell_size, cell_size, cell_size)

                    blocks.append(blocks[-1].copy())

                elif block.collidelist(blocks[1:]) > -1:
                    return score
            else:
                block.move_ip(blocks[-i-2].left-block.left, blocks[-i-2].top-block.top)

            if any([block.left < 0, block.right > width, block.top < 0, block.bottom > height]):
                return score

            pygame.draw.rect(screen, pygame.Color("brown"), block)
            pygame.draw.rect(screen, pygame.Color("black"), block, width=2)

        score_rect = pygame.draw.rect(screen, pygame.Color("orange"), (0, height, width, cell_size))

        font_block = font.render(score.__str__(), True, pygame.Color("black"))
        screen.blit(font_block, score_rect)

        pygame.draw.rect(screen, pygame.Color("red"), food)

        pygame.draw.rect(screen, pygame.Color("orange"), (height, 0, width, cell_size))

        pygame.display.update()
        clock.tick(framerate)


def show_start_screen(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if start_rectangle.collidepoint(pos):
                    return "GAME"

            elif event.type == pygame.KEYDOWN:
                return "GAME"

        screen.fill(pygame.Color("grey"))
        start_button = start_font.render("start", True, pygame.Color("black"))

        start_rectangle = start_button.get_rect(center=(width / 2, height // 3))

        screen.blit(start_button, start_rectangle)
        pygame.display.update()


framerate, cell_size, cell_number = read_settings()

height = cell_number * cell_size
width = cell_number * cell_size

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((height, width+cell_size))
start_font = pygame.font.SysFont("Arial", cell_size * 2)
font = pygame.font.SysFont("Arial", 20)

show_screen = "START"

while True:
    if show_screen == "START":
        show_screen = show_start_screen(screen)

        clock.tick(framerate)
    elif show_screen == "GAME":
        score = play_game(screen, cell_size, cell_number, font)
        show_screen = "START"