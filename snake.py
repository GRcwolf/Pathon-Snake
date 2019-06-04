from random import randint

import pygame

pygame.init()
pygame.display.set_caption('Python Python')

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 20
SPEED = 250
FPS = 60
SEGMENTS = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

FOOD_COLORS = [WHITE, GREEN, RED, BLUE]


class Snake:

    def __init__(self):
        self.x_pos = WINDOW_WIDTH / 2
        # while self.x_pos % BLOCK_SIZE != 0:
        #     self.x_pos -= 1
        self.y_pos = WINDOW_HEIGHT / 2
        # while self.y_pos % BLOCK_SIZE != 0:
        #     self.x_pos -= 1
        self.direction = 0
        self.segments = []
        for i in range(0, SEGMENTS):
            index = randint(1, len(FOOD_COLORS)) - 1
            self.grow(FOOD_COLORS[index])

    def move(self):
        if self.direction == 1:
            self.x_pos += SPEED / FPS
        elif self.direction == 2:
            self.y_pos += SPEED / FPS
        elif self.direction == 3:
            self.x_pos -= SPEED / FPS
        else:
            self.y_pos -= SPEED / FPS
        if self.y_pos > WINDOW_HEIGHT:
            self.y_pos -= WINDOW_HEIGHT
        elif self.y_pos < 0:
            self.y_pos += WINDOW_HEIGHT
        if self.x_pos > WINDOW_WIDTH:
            self.x_pos -= WINDOW_WIDTH
        elif self.x_pos < 0:
            self.x_pos += WINDOW_WIDTH

    def draw(self, window):
        for segment in self.segments:
            segment.draw(window)
        pygame.draw.rect(window, GREEN, (self.x_pos, self.y_pos, BLOCK_SIZE, BLOCK_SIZE))

    def update_directions(self):
        prev_direction = self.direction
        x, y = self.x_pos, self.y_pos
        self.segments[0].x_pos, self.segments[0].y_pos = x, y

        for i in range(1, len(self.segments)):
            segment = self.segments[i]
            tmp_direction = segment.direction
            segment.direction = prev_direction
            prev_direction = tmp_direction

            if segment.direction == 1:
                x -= BLOCK_SIZE
            elif segment.direction == 2:
                y -= BLOCK_SIZE
            elif segment.direction == 3:
                x += BLOCK_SIZE
            else:
                y += BLOCK_SIZE
            if y > WINDOW_HEIGHT:
                y -= WINDOW_HEIGHT
            elif y < 0:
                y += WINDOW_HEIGHT
            if x > WINDOW_WIDTH:
                x -= WINDOW_WIDTH
            elif x < 0:
                x += WINDOW_WIDTH
            segment.x_pos = x
            segment.y_pos = y

    def grow(self, color=GREEN):
        self.segments = [Segment(self.direction, color)] + self.segments


class Segment:
    def __init__(self, direction, color=GREEN):
        self.direction = direction
        self.color = color
        self.x_pos = WINDOW_HEIGHT
        self.y_pos = WINDOW_WIDTH

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x_pos, self.y_pos, BLOCK_SIZE, BLOCK_SIZE))


class Food:
    def __init__(self):
        self.x_pos = randint(BLOCK_SIZE, WINDOW_WIDTH)
        self.y_pos = randint(BLOCK_SIZE, WINDOW_HEIGHT)
        color_index = randint(0, len(FOOD_COLORS) - 1)
        self.color = FOOD_COLORS[color_index]

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x_pos, self.y_pos, BLOCK_SIZE, BLOCK_SIZE))


class Game:
    def __init__(self):
        self.last_direction_update = 0
        self.main()

    @staticmethod
    def check_collision(rect0, rect1):
        x0, y0, h0, w0 = rect0
        x1, y1, h1, w1 = rect1

        x0, y0 = int(x0), int(y0)
        x1, y1 = int(x1), int(y1)

        x_collides = False
        y_collides = False

        for x0_check in range(x0, x0 + w0):
            if x0_check in range(x1, x1 + w1):
                x_collides = True
        for y0_check in range(y0, y0 + h0):
            if y0_check in range(y1, y1 + h1):
                y_collides = True
        return y_collides and x_collides

    @staticmethod
    def check_food_collision(snake, food):
        if Game.check_collision((snake.x_pos, snake.y_pos, BLOCK_SIZE, BLOCK_SIZE),
                                (food.x_pos, food.y_pos, BLOCK_SIZE, BLOCK_SIZE)):
            snake.grow(food.color)
            food = Food()

        return snake, food

    def main(self):
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        play = True
        snake = Snake()
        food = Food()
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(BLACK)
        # snake.grow()
        # snake.grow(WHITE)
        while play:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    play = False
                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_w, pygame.K_UP] and not snake.direction == 2:
                        snake.direction = 0
                    if event.key in [pygame.K_RIGHT, pygame.K_d] and not snake.direction == 3:
                        snake.direction = 1
                    if event.key in [pygame.K_DOWN, pygame.K_s] and not snake.direction == 0:
                        snake.direction = 2
                    if event.key in [pygame.K_LEFT, pygame.K_a] and not snake.direction == 1:
                        snake.direction = 3
            self.last_direction_update += 1
            if self.last_direction_update >= BLOCK_SIZE / (SPEED / FPS):
                snake.update_directions()
                self.last_direction_update -= BLOCK_SIZE / (SPEED / FPS)

            snake, food = Game.check_food_collision(snake, food)
            window.fill(BLACK)
            food.draw(window)
            snake.move()
            snake.draw(window)
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    pygame.quit()
    quit()
