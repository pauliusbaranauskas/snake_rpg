import pygame
import pygame_menu as pm

import sys

from random import randint
import json

import os


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
    """Class to read, update, save settings.
    Takes everything from snake settings.json file and uses as attributes.
    """
    cell_number: int
    cell_size: int
    framerate: int

    def __init__(self):
        self.get_file_path()
        self.read_settings()

    def get_file_path(self):
        """Gets path to settings file.
        """
        file_path = os.path.realpath(__file__)
        sep = os.path.sep
        file_path = file_path.split(sep)
        file_path = file_path[:-1]
        assets_location = file_path.copy()
        assets_location.extend(["assets", ""])
        self.assets_location = sep.join(assets_location)
        file_path.append("snake settings.json")
        self.file_path = sep.join(file_path)

    def read_settings(self):
        """Reads settings from settings json.
        By default, this file is located in game directory as "snake settings.json" file.
        """
        with open(self.file_path) as f:
            settings = f.read()
            self.settings = json.loads(settings)
        for key, value in self.settings.items():
            setattr(self, key, value)

    def save_settings(self):
        """Saves settings to settings json file.
        By default, this file is located in game directory as "snake settings.json" file.
        """
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f)

    def update(self, attr, value):
        """Updates (or creates new) setting.

        Args:
            attr (str): Settings option/attribute.
            value (any): Any value to add/update.
        """
        self.settings[attr] = value
        setattr(self, attr, value)

    def update_numeric(self, attr, value):
        """Updates (or creates new) setting integer value. If provided value is not numeric, then saves 0.

        Args:
            attr (str): attribute/setting name.
            value (int): Integer value to add to settings.
        """
        try:
            value = int(value)
        except ValueError:
            value = 0
        self.update(attr, value)

    @property
    def height(self):
        """Vertical size of game area in pixels.

        Returns:
            int: Vertical size of game area in pixels.
        """
        return self.cell_number * self.cell_size

    @property
    def width(self):
        """Horizontal size of game area in pixels.

        Returns:
            int: Horizontal size of game area in pixels.
        """
        return self.cell_number * self.cell_size

    def revert(self):
        """Resets settings to last saved value.
        """
        self.__init__()

    def __str__(self):
        return self.settings.__str__()


class Food():
    def __init__(self, settings):
        self.cell_number = settings.cell_number
        self.cell_size = settings.cell_size
        self.food_rect = pygame.Rect(self.generate_coordinates())
        self.img = pygame.image.load("".join([settings.assets_location, "mouse.png"]))
        self.img.convert()

    def generate_coordinates(self):
        return randint(0, self.cell_number - 1) * self.cell_size, \
            randint(0, self.cell_number - 1) * self.cell_size, \
            self.cell_size, \
            self.cell_size

    def update(self, *args, **kwargs):
        self.food_rect.update(*args, **kwargs)

    def collidelist(self, rectangles):
        return self.food_rect.collidelist(rectangles)


class SnakeHead(pygame.Rect):
    def __init__(self, settings, x_pos, y_pos):
        self.settings = settings
        self.head = pygame.Rect(x_pos, y_pos, self.settings.cell_size, self.settings.cell_size)
        self.img_original = pygame.image.load("".join([settings.assets_location, "head.png"]))
        self.img_original.convert()
        self.img = self.img_original.copy()

    def rotate(self, x_step, y_step):
        if x_step == self.settings.cell_size:
            self.img = self.img_original.copy()
        elif x_step == -self.settings.cell_size:
            self.img = pygame.transform.rotate(self.img_original, 180)
        elif y_step == -self.settings.cell_size:
            self.img = pygame.transform.rotate(self.img_original, 90)
        elif y_step == self.settings.cell_size:
            self.img = pygame.transform.rotate(self.img_original, 270)

class SnakeBody(pygame.Rect):

    def __init__(self, settings, x_pos, y_pos):
        self.settings = settings
        self.body_block = pygame.Rect(x_pos, y_pos, self.settings.cell_size, self.settings.cell_size)



def play_game():
    """Displays and updates game screen. Contains all game logic.

    Returns:
        int: Score when game is stopped.
    """
    settings = Settings()

    x_step = settings.cell_size
    y_step = 0
    score = 0

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.width, settings.height + settings.cell_size))

    food = Food(settings)
    snake_head = SnakeHead(settings, 0+settings.cell_size, 0)
    snake_body = SnakeBody(settings, 0, 0)
    blocks = [snake_head.head,
             snake_body.body_block]
    font = pygame.font.SysFont("Arial", 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_main_menu()

            elif event.type == pygame.KEYDOWN:
                x_step, y_step = direction(event, settings.cell_size, x_step, y_step)
                snake_head.rotate(x_step, y_step)
                if x_step == y_step:
                    show_game_over(score)

        screen.fill(pygame.Color("grey"))

        for i, block in enumerate(reversed(blocks)):
            if i == len(blocks) - 1:
                block.move_ip(x_step, y_step)
                if pygame.Rect.colliderect(snake_head.head, food.food_rect):
                    food.update(food.generate_coordinates())

                    score += 1

                    while food.collidelist(blocks) > -1:
                        food.update(food.generate_coordinates())

                    blocks.append(blocks[-1].copy())

                elif block.collidelist(blocks[1:]) > -1:
                    show_game_over(score)
                screen.blit(snake_head.img, snake_head.head)

            else:
                block.move_ip(blocks[-i - 2].left - block.left, blocks[-i - 2].top - block.top)
                pygame.draw.rect(screen, pygame.Color("brown"), block)
                pygame.draw.rect(screen, pygame.Color("black"), block, width=2)
            if any([block.left < 0, block.right > settings.width, block.top < 0, block.bottom > settings.height]):
                show_game_over(score)

        score_rect = pygame.draw.rect(screen, pygame.Color("orange"),
                                      (0, settings.height, settings.width, settings.cell_size))

        screen.blit(food.img, food.food_rect)

        font_block = font.render(score.__str__(), True, pygame.Color("black"))
        screen.blit(font_block, score_rect)

        pygame.draw.rect(screen, pygame.Color("grey"), food.food_rect, 1)

        pygame.draw.rect(screen, pygame.Color("orange"), (settings.height, 0, settings.width, settings.cell_size))

        pygame.display.update()
        clock.tick(settings.framerate)


def show_settings():
    """Displays settings (uses pygame_menu module).
    """
    # https: // www.geeksforgeeks.org / create - settings - menu - in -python - pygame /
    settings = Settings()

    screen = pygame.display.set_mode((settings.width, settings.height))

    settings_menu = pm.Menu(title="Settings", width=settings.width, height=settings.height)
    settings_menu.add.text_input(title="Speed: ",
                                 default=str(settings.framerate),
                                 onchange=lambda value: settings.update_numeric("framerate", value)
                                 )

    settings_menu.add.text_input(title="cell size: ", default=str(settings.cell_size), onchange=lambda value: settings.update_numeric("cell_size", value))
    settings_menu.add.text_input(title="Number of cells: ", default=str(settings.cell_number), onchange=lambda value: settings.update_numeric("cell_number", value))

    settings_menu.add.label("")
    settings_menu.add.button(title="SAVE", action=settings.save_settings)
    settings_menu.add.button(title="Revert to last saved", action=show_settings)
    settings_menu.add.button(title="Cancel", action=show_main_menu)


    settings_menu.mainloop(screen)


def show_main_menu():
    """Displays main menu (uses pygame_menu module).
    """
    settings = Settings()
    screen = pygame.display.set_mode((settings.width, settings.height))

    main_menu = pm.Menu(title="Snake RPG"
                        , width=settings.width
                        , height=settings.height)

    main_menu.add.label("Current HIGH SCORE:")
    main_menu.add.label(settings.high_score)
    main_menu.add.label("")
    main_menu.add.label("")
    main_menu.add.label("")

    main_menu.add.button(title="PLAY", action=play_game)

    main_menu.add.button(title="Settings", action=show_settings)
    main_menu.add.button(title="Quit", action=pm.events.EXIT)

    main_menu.mainloop(screen)

def show_game_over(score):
    """Displays GAME OVER screen with score and options to retry or quit.

    Args:
        score (int): Score of last game.
    """
    settings = Settings()
    screen = pygame.display.set_mode((settings.width, settings.height + settings.cell_size))
    game_over_menu = pm.Menu(title="GAME OVER", width=settings.width, height=settings.height)
    if score > settings.high_score:
        settings.update_numeric("high_score", score)
        settings.save_settings()
        game_over_menu.add.label("New HIGH SCORE:")
    else:
        game_over_menu.add.label("Your score:")

    game_over_menu.add.label(score)
    game_over_menu.add.label("")
    game_over_menu.add.label("")

    game_over_menu.add.button(title="Retry", action=play_game)
    game_over_menu.add.button(title="Main Menu", action=show_main_menu)

    game_over_menu.add.button(title="QUIT", action=pm.events.EXIT)

    game_over_menu.mainloop(screen)

pygame.init()

play_game()