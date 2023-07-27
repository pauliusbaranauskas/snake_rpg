import pygame
import sys

from random import randint


cell_size = 40
cell_number = 20

height = cell_number * cell_size
width = cell_number * cell_size
framerate = 10

pygame.init()

screen = pygame.display.set_mode((height, width+cell_size))

clock = pygame.time.Clock()
x_pos = 0
y_pos = 0

x_step = cell_size
y_step = 0

score = 0

def end_game():
    pygame.quit()
    sys.exit()

food = pygame.Rect(randint(0, cell_number-1)*cell_size, randint(0, cell_number-1)*cell_size, cell_size, cell_size)

blocks = [pygame.Rect(x_pos+cell_size, y_pos, cell_size, cell_size),pygame.Rect(x_pos, y_pos, cell_size, cell_size)]

font = pygame.font.SysFont("Arial", 20)

while True:
    snake_length = len(blocks)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end_game()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if y_step == -cell_size:
                    end_game()
                else:
                    x_step, y_step = 0, cell_size
            elif event.key == pygame.K_LEFT:
                if x_step == cell_size:
                    end_game()
                else:
                    x_step, y_step = -cell_size, 0
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

    screen.fill(pygame.Color("grey"))

    for i, block in enumerate(reversed(blocks)):
        if i == len(blocks)-1:
            block.move_ip(x_step, y_step)
            if pygame.Rect.colliderect(block, food):
                food.update(randint(0, cell_number-1)*cell_size, randint(0, cell_number-1)*cell_size, cell_size, cell_size)

                score += 1


                while food.collidelist(blocks) > -1:
                    food.update(randint(0, cell_number - 1) * cell_size, randint(0, cell_number - 1) * cell_size, cell_size, cell_size)
                print(score)

                blocks.append(blocks[-1].copy())

            elif block.collidelist(blocks[1:]) > -1:
                end_game()
        else:
            block.move_ip(blocks[-i-2].left-block.left, blocks[-i-2].top-block.top)



        if any([block.left < 0, block.right > width, block.top < 0, block.bottom > height]):
            end_game()



        pygame.draw.rect(screen, pygame.Color("brown"), block)
        pygame.draw.rect(screen, pygame.Color("black"), block, width=2)

    score_rect = pygame.draw.rect(screen, pygame.Color("orange"), (0, height, width, cell_size))

    font_block = font.render(score.__str__(), True, pygame.Color("black"))
    screen.blit(font_block, score_rect)

    pygame.draw.rect(screen, pygame.Color("red"), food)

    pygame.draw.rect(screen, pygame.Color("orange"), (height, 0, width, cell_size))

    pygame.display.update()


    clock.tick(framerate)