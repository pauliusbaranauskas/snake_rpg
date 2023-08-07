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
            x_step, y_step = -1, -1
        else:
            x_step, y_step = -cell_size, 0
    elif event.key == pygame.K_UP:
        if y_step == cell_size:
            x_step, y_step = -1, -1
        else:
            x_step, y_step = 0, -cell_size
    elif event.key == pygame.K_RIGHT:
        if x_step == -cell_size:
            x_step, y_step = -1, -1
        else:
            x_step, y_step = cell_size, 0

    return x_step, y_step


class Settings():
    cell_number: int
    cell_size: int
    framerate: int

    def __init__(self):
        self.get_file_path()
        self.read_settings()

    def get_file_path(self):
        file_path = os.path.realpath(__file__)
        sep = os.path.sep
        file_path = file_path.split(sep)
        file_path = file_path[:-1]
        file_path.append("snake settings.json")
        self.file_path = sep.join(file_path)

    def read_settings(self):
        with open(self.file_path) as f:
            settings = f.read()
            self.settings = json.loads(settings)
        for key, value in self.settings.items():
            setattr(self, key, value)

    def save_settings(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f)

    def update(self, attr, value):
        self.settings[attr] = value
        setattr(self, attr, value)

    def update_numeric(self, attr, value):
        try:
            value = int(value)
        except ValueError:
            value = 0
        self.update(attr, value)

    @property
    def height(self):
        return self.cell_number * self.cell_size

    @property
    def width(self):
        return self.cell_number * self.cell_size

    def revert(self):
        self.__init__()

    def __str__(self):
        return self.settings.__str__()

def play_game():
    """Displays and updates game screen. Contains all game logic.

    Args:
        screen (pygame.display): Application screen.
        setting (dict): dictionary containing game settings.

    Returns:
        int: Score when game is stopped.
    """
    settings = Settings()

    x_step = settings.cell_size
    y_step = 0
    score = 0

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.width, settings.height + settings.cell_size))

    food = pygame.Rect(randint(0, settings.cell_number - 1) * settings.cell_size,
                       randint(0, settings.cell_number - 1) * settings.cell_size, settings.cell_size,
                       settings.cell_size)

    blocks = [pygame.Rect(0 + settings.cell_size, 0, settings.cell_size, settings.cell_size),
              pygame.Rect(0, 0, settings.cell_size, settings.cell_size)]
    font = pygame.font.SysFont("Arial", 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_main_menu()

            elif event.type == pygame.KEYDOWN:
                x_step, y_step = direction(event, settings.cell_size, x_step, y_step)
                if x_step == y_step:
                    show_main_menu()

        screen.fill(pygame.Color("grey"))

        for i, block in enumerate(reversed(blocks)):
            if i == len(blocks) - 1:
                block.move_ip(x_step, y_step)
                if pygame.Rect.colliderect(block, food):
                    food.update(randint(0, settings.cell_number - 1) * settings.cell_size,
                                randint(0, settings.cell_number - 1) * settings.cell_size, settings.cell_size,
                                settings.cell_size)

                    score += 1

                    while food.collidelist(blocks) > -1:
                        food.update(randint(0, settings.cell_number - 1) * settings.cell_size,
                                    randint(0, settings.cell_number - 1) * settings.cell_size, settings.cell_size,
                                    settings.cell_size)

                    blocks.append(blocks[-1].copy())

                elif block.collidelist(blocks[1:]) > -1:
                    show_main_menu()
            else:
                block.move_ip(blocks[-i - 2].left - block.left, blocks[-i - 2].top - block.top)

            if any([block.left < 0, block.right > settings.width, block.top < 0, block.bottom > settings.height]):
                show_main_menu()

            pygame.draw.rect(screen, pygame.Color("brown"), block)
            pygame.draw.rect(screen, pygame.Color("black"), block, width=2)

        score_rect = pygame.draw.rect(screen, pygame.Color("orange"),
                                      (0, settings.height, settings.width, settings.cell_size))

        font_block = font.render(score.__str__(), True, pygame.Color("black"))
        screen.blit(font_block, score_rect)

        pygame.draw.rect(screen, pygame.Color("red"), food)

        pygame.draw.rect(screen, pygame.Color("orange"), (settings.height, 0, settings.width, settings.cell_size))

        pygame.display.update()
        clock.tick(settings.framerate)


def show_settings():
    # https: // www.geeksforgeeks.org / create - settings - menu - in -python - pygame /
    settings = Settings()

    screen = pygame.display.set_mode((settings.width, settings.height))

    settings_menu = pm.Menu(title="Settings", width=settings.width, height=settings.height)
    settings_menu.add.text_input(title="Speed: ", default=str(settings.framerate), onchange=lambda value: settings.update_numeric("framerate", value))

    settings_menu.add.text_input(title="cell size: ", default=str(settings.cell_size), onchange=lambda value: settings.update_numeric("cell_size", value))
    settings_menu.add.text_input(title="Number of cells: ", default=str(settings.cell_number), onchange=lambda value: settings.update_numeric("cell_number", value))

    settings_menu.add.label("")
    settings_menu.add.button(title="SAVE", font_color=(0, 0, 0), action=settings.save_settings)
    settings_menu.add.button(title="Revert to last saved", font_color=(0, 0, 0), action=show_settings)
    settings_menu.add.button(title="Cancel", font_color=(0, 0, 0), action=show_main_menu)

    settings_menu.mainloop(screen)


def show_main_menu():
    settings = Settings()
    screen = pygame.display.set_mode((settings.width, settings.height))

    main_menu = pm.Menu(title="Snake RPG"
                        , width=settings.width
                        , height=settings.height)

    main_menu.add.button(title="PLAY", font_color=(0, 0, 0), action=play_game)

    main_menu.add.button(title="Settings", font_color=(0, 0, 0), action=show_settings)
    main_menu.add.button(title="Quit", font_color=(0, 0, 0), action=pm.events.EXIT)

    main_menu.mainloop(screen)


# show_screen = "SETTINGS"
pygame.init()

show_screen = show_main_menu()
