import pygame
import pygame_menu as pm

import sys

from random import randint
import json

import os


def end_game():
    """
    Kills entire app.
    """
    pygame.quit()
    sys.exit()


def read_settings():
    """Reads settings json file and returns settings as dictionary.

    Returns:
        dict: Settings dictionary.
    """
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
    """Updates snake movement direction by arrow button clicks.

    Args:
        event (pygame.event): Pygame event object.
        cell_size (int): Size of cell. It describe step size.
        x_step (int): Current snake movement speed in horizontal direction.
        y_step (int): Current snake movement speed in vertical direction.

    Returns:
        int, int: Updated snake movement speeds in horizontal and vertical directions.
    """
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


def play_game():
    """Displays and updates game screen. Contains all game logic.

    Args:
        screen (pygame.display): Application screen.
        setting (dict): dictionary containing game settings.

    Returns:
        int: Score when game is stopped.
    """
    settings = read_settings()

    cell_size = settings["cell_size"]
    cell_number = settings["cell_number"]
    height = cell_number * cell_size
    width = cell_number * cell_size
    x_step = cell_size
    y_step = 0
    score = 0

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((height, width + cell_size))

    food = pygame.Rect(randint(0, cell_number-1)*cell_size, randint(0, cell_number-1)*cell_size, cell_size, cell_size)

    blocks = [pygame.Rect(0+cell_size, 0, cell_size, cell_size),pygame.Rect(0, 0, cell_size, cell_size)]
    font = pygame.font.SysFont("Arial", 20)

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


def get_number_input(event, number):
    """Reads and updates numeric input in settings screen.

    Args:
        event (pygame.event): Pygame event.
        number (str): Displayed number in setting rectangle.

    Returns:
        str, Bool: Updated displayed number and field status. True means field is still active and accepts inputs.
    """
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
    """Reverses field status. True means field accepts new inputs, False - not anymore.

    Args:
        active (Bool): True - accepts inputs, False - does not accept.

    Returns:
        Bool: True - accepts inputs, False - does not accept.
    """
    if active:
        return False
    else:
        return True


def show_settings():
    """Displays and contains all settings menu.

    Args:
        screen (pygame.display): Application screen.
        height (int): Application hight in pixels.
        width (int): Application width in pixels.
        settings (dict): Settings dictionary.
    """
    settings = read_settings()

    height = settings["cell_number"] * settings["cell_size"]
    width = settings["cell_number"] * settings["cell_size"]
    screen = pygame.display.set_mode((width, height))

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

        save_button_text = settings_font.render("CANCEL", True, pygame.Color("black"))

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


def show_main_menu():
    settings = read_settings()
    screen = pygame.display.set_mode((settings["cell_number"]*settings["cell_size"], settings["cell_number"]*settings["cell_size"]))

    main_menu = pm.Menu(title="Snake RPG"
                        , width=settings["cell_number"]*settings["cell_size"]
                        , height=settings["cell_number"]*settings["cell_size"])

    main_menu.add.button(title="PLAY", font_color=(0, 0, 0), action=play_game)

    main_menu.add.button(title="Settings", font_color=(0, 0, 0), action=show_settings)
    main_menu.add.button(title="Quit", font_color=(0, 0, 0), action=pm.events.EXIT)

    main_menu.mainloop(screen)

show_screen = "START"
pygame.init()

while True:
    if show_screen == "START":
        show_screen = show_main_menu()

    elif show_screen == "GAME":
        score = play_game()
        show_screen = "START"

    elif show_screen == "SETTINGS":
        show_screen, settings = show_settings()
