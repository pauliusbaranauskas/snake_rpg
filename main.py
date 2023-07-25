import pygame
import sys


cell_size = 40
cell_number = 20

height = cell_number * cell_size
width = cell_number * cell_size
framerate = 12

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

class snake:
    def __init__(self, x_pos, y_pos, x_step, y_step, cell_size):
        self.cell_size = cell_size
        self.x_pos, self.y_pos = x_pos, y_pos
        self.x_step, self.y_step = x_step, y_step

    def update_speed(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.y_step == -self.cell_size:
                    end_game()
                else:
                    self.x_step, self.y_step = 0, self.cell_size
                    # x_step = 0
            elif event.key == pygame.K_UP:
                if self.y_step == self.cell_size:
                    end_game()
                else:
                    self.x_step, self.y_step = 0, -self.cell_size
            elif event.key == pygame.K_RIGHT:
                if self.x_step == -self.cell_size:
                    end_game()
                else:
                    self.x_step, self.y_step = self.cell_size, 0
            elif event.key == pygame.K_LEFT:
                if self.x_step == self.cell_size:
                    end_game()
                else:
                    self.x_step, self.y_step = -self.cell_size, 0

        self.x_pos += self.x_step
        self.y_pos += self.y_step
        self.check_bounds(width, height)

    def get_coordinates(self):
        return self.x_pos, self.y_pos
    
    def get_speed(self):
        return self.x_step, self.y_step

    def get_rect_tuple(self):
        return [self.x_pos, self.y_pos, self.cell_size, self.cell_size]

    def check_bounds(self, height, width):
        print(self.x_pos, self.y_pos)
        if any([self.x_pos < 0, self.x_pos >= width, self.y_pos < 0, self.y_pos >= height]):
            end_game()


blocks = [snake(x_pos, y_pos, x_step, y_step, cell_size)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()
    screen.fill(pygame.Color("grey"))
    
    for block in blocks:
        block.update_speed(event)
        block.check_bounds(*screen.get_size())
        pygame.draw.rect(screen, pygame.Color("green"), block.get_rect_tuple())
    



    pygame.display.update()


    clock.tick(framerate)