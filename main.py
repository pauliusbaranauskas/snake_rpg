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
        return json.loads(settings)


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


def show_start_screen(screen, width, height):
    start_screen_font = pygame.font.SysFont("Arial", cell_size * 2)
    start_button = start_screen_font.render("start", True, pygame.Color("black"))

    settings_button = start_screen_font.render("settings", True, pygame.Color("black"))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if start_rectangle.collidepoint(pos):
                    return "GAME"

                elif settings_rectangle.collidepoint(pos):
                    return "SETTINGS"

            elif event.type == pygame.KEYDOWN:
                return "GAME"

        screen.fill(pygame.Color("grey"))

        start_rectangle = start_button.get_rect(center=(width // 2, height // 3))

        screen.blit(start_button, start_rectangle)

        settings_rectangle = settings_button.get_rect(center=(width//2, height//3*2))
        screen.blit(settings_button, settings_rectangle)

        pygame.display.update()


def get_number_input(event, number):
    if event.key == pygame.K_RETURN:
        return number, False
    elif event.key == pygame.K_BACKSPACE:
        return number[:-1], True
    elif event.unicode.isdigit():
        return "".join([number.__str__(), event.unicode]), True
    elif event.key == pygame.K_ESCAPE:
        return number, False
    else:
        return number, True


def frame_activation(active):
    if active:
        return False
    else:
        return True


def show_settings(screen, height, width, settings):
    cell_size = settings["cell_size"].__str__()
    framerate = settings["speed"].__str__()
    cell_number = settings["cell_number"].__str__()
    settings_font = pygame.font.SysFont("Arial", int(cell_size))
    framerate_active = False
    cell_size_active = False
    cell_number_active = False


    while True:

        framerate_rect = pygame.Rect((width // 3, 0, width // 3, int(cell_size)))
        framerate_text = settings_font.render("speed", True, pygame.Color("black"))
        framerate_input_text = settings_font.render(framerate, True, pygame.Color("white"))
        framerate_input_rect = pygame.Rect(framerate_text.get_rect(topleft=framerate_rect.topright))
        framerate_input_rect.height = int(cell_size)

        cell_size_rect = pygame.Rect((width // 3, int(cell_size), width // 3, int(cell_size)))
        cell_size_text = settings_font.render("cell size in pixels", True, pygame.Color("black"))
        cell_size_input_text = settings_font.render(cell_size, True, pygame.Color("white"))
        cell_size_input_rect = pygame.Rect(cell_size_text.get_rect(topleft=cell_size_rect.topright))
        cell_size_input_rect.height = int(cell_size)

        cell_number_rect = pygame.Rect((width // 3, int(cell_size)*2, width // 3, int(cell_size)))
        cell_number_text = settings_font.render("cell count", True, pygame.Color("black"))
        cell_number_input_text = settings_font.render(cell_number, True, pygame.Color("white"))
        cell_number_input_rect = pygame.Rect(cell_number_text.get_rect(topleft=cell_number_rect.topright))
        cell_number_input_rect.height = int(cell_size)


        screen.fill(pygame.Color("grey"))
        pygame.draw.rect(screen, pygame.Color("grey"), framerate_rect)
        pygame.draw.rect(screen, pygame.Color("grey"), cell_size_rect)
        pygame.draw.rect(screen, pygame.Color("grey"), cell_number_rect)




        if framerate_active:
            pygame.draw.rect(screen, pygame.Color("blue"), framerate_input_rect)
        else:
            pygame.draw.rect(screen, pygame.Color("blue4"), framerate_input_rect)

        if cell_size_active:
            pygame.draw.rect(screen, pygame.Color("blue"), cell_size_input_rect)
        else:
            pygame.draw.rect(screen, pygame.Color("blue4"), cell_size_input_rect)

        if cell_number_active:
            pygame.draw.rect(screen, pygame.Color("blue"), cell_number_input_rect)
        else:
            pygame.draw.rect(screen, pygame.Color("blue4"), cell_number_input_rect)

        screen.blit(framerate_text, framerate_rect)
        screen.blit(framerate_input_text, framerate_input_rect)
        screen.blit(cell_size_text, cell_size_rect)
        screen.blit(cell_size_input_text, cell_size_input_rect)
        screen.blit(cell_number_text, cell_number_rect)
        screen.blit(cell_number_input_text, cell_number_input_rect)


        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end_game()
            elif event.type == pygame.KEYDOWN:
                if framerate_active:
                    framerate, framerate_active = get_number_input(event, framerate)

                elif cell_size_active:
                    cell_size, cell_size_active = get_number_input(event, cell_size)

                elif cell_number_active:
                    cell_number, cell_number_active = get_number_input(event, cell_number)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                if framerate_input_rect.collidepoint(pos):
                    framerate_active = frame_activation(framerate_active)
                    cell_size_active = False
                    cell_number_active = False

                elif cell_size_input_rect.collidepoint(pos):
                    cell_size_active = frame_activation(cell_size_active)
                    framerate_active = False
                    cell_number_active = False

                elif cell_number_input_rect.collidepoint(pos):
                    cell_number_active = frame_activation(cell_number_active)
                    framerate_active = False
                    cell_size_active = False



settings = read_settings()

framerate = settings["speed"]
cell_size = settings["cell_size"]
cell_number = settings["cell_number"]

height = cell_number * cell_size
width = cell_number * cell_size

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((height, width+cell_size))
font = pygame.font.SysFont("Arial", 20)

show_screen = "START"

while True:
    if show_screen == "START":
        show_screen = show_start_screen(screen, height, width)

        clock.tick(framerate)
    elif show_screen == "GAME":
        score = play_game(screen, cell_size, cell_number, font)
        show_screen = "START"

    elif show_screen == "SETTINGS":
        show_screen, settings = show_settings(screen, height, width, settings)
        framerate = settings["speed"]
        cell_size = settings["cell_size"]
        cell_number = settings["cell_number"]
