import pygame
import pygame_menu as pm

from random import randint
import json

import os

from utils.settings import Settings
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
    elif event.key == pygame.K_ESCAPE:
        x_step, y_step = 0, 0

    return x_step, y_step

class Food():
    """A class that represent a food item that the snake is eating.
    """
    def __init__(self, settings):
        self.cell_number = settings.cell_number
        self.cell_size = settings.cell_size
        self.food_rect = pygame.Rect(self.generate_coordinates())
        self.img = pygame.image.load("".join([settings.assets_location, "mouse.png"]))
        self.img.convert()

    def generate_coordinates(self):
        """Generates new coordinates for food rectangle.

        Returns:
            tuple: New coordinates that can be used to move food rectangle.
        """
        return randint(0, self.cell_number - 1) * self.cell_size, \
            randint(0, self.cell_number - 1) * self.cell_size, \
            self.cell_size, \
            self.cell_size

    def update(self, *args, **kwargs):
        """Updates location of food rectangle.
        """
        self.food_rect.update(*args, **kwargs)

    def collidelist(self, rectangles):
        """Redirects to pygame.rect.collidelist method that can be used to check
        if a list of rectangles overlap.

        Args:
            rectangles (list): List of rectangles to check overlap.

        Returns:
            list: List of indices that represent positions of rectangles that
            overlap with self rectangle.
        """
        return self.food_rect.collidelist(rectangles)


class SnakeHead(pygame.Rect):
    """Class object for snake head rectangle.
    Inherits pygame.Rect class.
    """
    def __init__(self, settings, x_pos, y_pos):
        self.settings = settings

        self.head = pygame.Rect(x_pos, y_pos, self.settings.cell_size, self.settings.cell_size)
        self.img_original = pygame.image.load("".join([settings.assets_location, "head.png"]))
        self.img_original.convert()
        self.img = self.img_original.copy()

    def rotate(self, x_step, y_step):
        """Rotates snake's head depending on direction that it should be moving to.

        Args:
            x_step (int): Speed on X axis.
            y_step (int): Speed on Y axis.
        """
        if x_step == self.settings.cell_size:
            self.img = self.img_original.copy()
        elif x_step == -self.settings.cell_size:
            self.img = pygame.transform.rotate(self.img_original, 180)
        elif y_step == -self.settings.cell_size:
            self.img = pygame.transform.rotate(self.img_original, 90)
        elif y_step == self.settings.cell_size:
            self.img = pygame.transform.rotate(self.img_original, 270)

    def move_ip(self, x, y):
        """Redirects to pygame.rect.move_ip method to change coordinates of the snake head.

        Args:
            x (int): New horizontal coordinates.
            y (int): New vertical coordinates.
        """
        self.head.move_ip(x, y)

    @property
    def top(self):
        return self.head.top

    @property
    def left(self):
        return self.head.left

    @property
    def right(self):
        return self.head.right

    @property
    def bottom(self):
        return self.head.bottom

    @property
    def midtop(self):
        return self.head.midtop

    @property
    def midleft(self):
        return self.head.midleft

    @property
    def midright(self):
        return self.head.midright

    @property
    def midbottom(self):
        return self.head.midbottom

class SnakeBody(pygame.Rect):
    """Class object for snake body structure. Each block is pygame.Rect object.
    Inherits pygame.Rect class.
    """
    def __init__(self, settings, x_pos, y_pos):
        self.settings = settings
        self.body = [pygame.Rect(x_pos, y_pos, self.settings.cell_size, self.settings.cell_size)]

        self.img_original = pygame.image.load("".join([settings.assets_location, "Body Straight.png"]))
        self.img_original.convert()

        self.img_bend_inside = pygame.image.load("".join([settings.assets_location, "Body bend inside.png"]))
        self.img_bend_inside.convert()
        self.img_bend_outside = pygame.image.load("".join([settings.assets_location, "Body bend outside.png"]))
        self.img_bend_outside.convert()

        self.img_tail = pygame.image.load("".join([settings.assets_location, "Body end.png"]))
        self.img_tail.convert()
        self.grow = False



    def draw(self, screen, head):
        """Displays snake's body. Excluding head.

        Args:
            screen (pygame.display): Mandatory parameter for pygame.
            head (head): Snake's Head object that represents snake's head's rectangle.
        """
        for i, body_block in enumerate(self.body):
            if i == 0:
                prior_block = head
            elif len(self.body) > 1:
                prior_block = self.body[i-1]

            if len(self.body)-1 == i:
                image = self.img_tail.copy()

                if body_block.midbottom == prior_block.midtop:
                    image = pygame.transform.rotate(image, 270)
                elif body_block.midleft == prior_block.midright:
                    image = pygame.transform.rotate(image, 180)
                elif body_block.midtop == prior_block.midbottom:
                    image = pygame.transform.rotate(image, 90)

            elif (body_block.midbottom == prior_block.midtop) & (body_block.midtop == self.body[i+1].midbottom):
                image = self.img_original.copy()
                image = pygame.transform.rotate(image, 90)
            elif (body_block.midtop == prior_block.midbottom) & (body_block.midbottom == self.body[i+1].midtop):
                image = self.img_original.copy()
                image = pygame.transform.rotate(image, 270)
            elif (body_block.midleft == prior_block.midright) & (body_block.midright == self.body[i+1].midleft):
                image = self.img_original.copy()
            elif (body_block.midright == prior_block.midleft) & (body_block.midleft == self.body[i+1].midright):
                image = self.img_original.copy()
                image = pygame.transform.rotate(image, 180)
            else:
                next_block = self.body[i+1]
                if body_block.midbottom == prior_block.midtop:
                    if body_block.midleft == next_block.midright:
                        image = self.img_bend_inside.copy()
                    elif body_block.midright == next_block.midleft:
                        image = self.img_bend_outside.copy()
                        image = pygame.transform.rotate(image, 90)

                elif body_block.midleft == prior_block.midright:
                    if body_block.midtop == next_block.midbottom:
                        image = self.img_bend_inside.copy()
                        image = pygame.transform.rotate(image, -90)
                    elif body_block.midbottom == next_block.midtop:
                        image = self.img_bend_outside.copy()

                elif body_block.midtop == prior_block.midbottom:
                    if body_block.midright == next_block.midleft:
                        image = self.img_bend_inside.copy()
                        image = pygame.transform.rotate(image, 180)
                    elif body_block.midleft == next_block.midright:
                        image = self.img_bend_outside.copy()
                        image = pygame.transform.rotate(image, -90)


                else:
                    if body_block.midbottom == next_block.midtop:
                        image = self.img_bend_inside.copy()
                        image = pygame.transform.rotate(image, 90)
                    else:
                        image = self.img_bend_outside.copy()
                        image = pygame.transform.rotate(image, 180)



            screen.blit(image, body_block)

    def move(self, head):
        """Updates snake's body's coordinates following snake's head's path.

        Args:
            head (Head): Snake's head object representing snake's body.
        """
        body_new = []
        for i, block in enumerate(reversed(self.body)):
            if (i == 0) & self.grow:
                body_new.append(block.copy())
                self.grow = False
            if i == len(self.body) - 1:
                block.move_ip(head.left-block.left, head.top-block.top)
            else:
                block.move_ip(self.body[-i-2].left-block.left, self.body[-i-2].top-block.top)

            body_new.append(block)

        self.body = list(reversed(body_new))

def show_map_maker():
    settings = Settings()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.width, settings.height + settings.cell_size))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_main_menu()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                show_main_menu()
                # Exists map builder on esc key press. Does not save the map.
        screen.fill(pygame.Color("grey"))
        pygame.display.update()
        clock.tick(settings.framerate)

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

        snake_head.move_ip(x_step, y_step)
        if pygame.Rect.colliderect(snake_head.head, food.food_rect):
            food.update(food.generate_coordinates())

            score += 1
            snake_body.grow = True
            while (food.collidelist(snake_body.body) > -1) or (food.collidelist([snake_head]) > -1):
                food.update(food.generate_coordinates())

        elif snake_head.head.collidelist(snake_body.body) > -1:
            show_game_over(score)
        screen.blit(snake_head.img, snake_head.head)


        snake_body.draw(screen, snake_head)
        snake_body.move(snake_head)

        if any([snake_head.left < snake_head.right > settings.width, snake_head.top < 0, snake_head.bottom > settings.height, snake_head.left < 0]):
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
    main_menu.add.button(title="Map Maker", action=show_map_maker)
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

show_main_menu()
