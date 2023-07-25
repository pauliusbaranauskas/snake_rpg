import pygame
import sys


cell_size = 40
cell_number = 20

height = cell_number * cell_size
width = cell_number * cell_size
framerate = 120

pygame.init()

# Display is display surface.
# There can be only one display surface.
# It is a canvas for entire game.
screen = pygame.display.set_mode((height, width))

# Surfaces are layers that can display graphics. There are multiple surfaces.
# It is not displayed by default.
# You first need to create a surface. Then you need to display it.

# Ways to create a surface:
# 1. Import image.
# 2. Creating any text.
# 3. Create empty surface.


# Clock object reikalingas, kad apriboti fps.
clock = pygame.time.Clock()
x_pos = 0
y_pos = 0

x_step = 0
y_step = 0
def end_game():
    pygame.quit()
    sys.exit()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if y_step == -cell_size:
                    end_game()
                else:
                    x_step, y_step = 0, cell_size
                    # x_step = 0
            elif event.key == pygame.K_UP:
                if y_step == cell_size:
                    end_game()
                else:
                    x_step, y_step = 0, -cell_size
            elif event.key == pygame.K_RIGHT:
                if x_step == -cell_size:
                    end_game()
                else:
                    x_step, y_step = cell_size, 0
            elif event.key == pygame.K_LEFT:
                if x_step == cell_size:
                    end_game()
                else:
                    x_step, y_step = -cell_size, 0


    x_pos += x_step
    y_pos += y_step
    if any([x_pos < 0, x_pos >= width, y_pos < 0, y_pos >= height]):
        end_game()

    screen.fill(pygame.Color("grey"))
    pygame.draw.rect(screen, pygame.Color("green"), (x_pos, y_pos, cell_size, cell_size))
    pygame.time.wait(100)




    pygame.display.update()


    clock.tick(framerate)