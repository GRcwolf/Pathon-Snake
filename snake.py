from random import randint

import math
import pygame

# Define some constants.
FONT_SIZE = 50
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
BLOCK_SIZE = 10
SPEED = 250
FPS = 50
SEGMENTS = 3

# Define the colors.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)

FOOD_COLORS = [WHITE, GREEN, BLUE, PURPLE]

pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Comic Sans MS', FONT_SIZE)
pygame.display.set_caption('Python Python')


class Snake:

    def __init__(self):
        """
        Initialized a Snake object.
        """
        self.x_pos = WINDOW_WIDTH / 2
        self.y_pos = WINDOW_HEIGHT / 2
        self.direction = 0
        self.segments = []
        self.segment_colors = [GREEN]
        self.segment_position = [(self.x_pos, self.y_pos + BLOCK_SIZE)]
        for i in range(0, SEGMENTS):
            index = randint(1, len(FOOD_COLORS)) - 1
            self.grow(FOOD_COLORS[index])

    def move(self):
        """
        Let the snake move on each frame.
        """
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
        """
        Draws the snake.

        :param window:
        """
        if len(self.segment_position) != len(self.segment_colors):
            print('An error happened')
            quit(1)

        for i in range(0, len(self.segment_position)):
            x, y = self.segment_position[i]
            Game.draw_rect(window, int(x), int(y), self.segment_colors[i])

    def update_directions_if_necessary(self):
        """
        Check if the directions of the segments have to be updated and does so if needed.
        """
        x1, y1 = self.segment_position[0]
        x0, y0 = self.x_pos, self.y_pos
        changes_occurred = False

        if (y1 - BLOCK_SIZE > y0 or y0 - y1 > 2 * BLOCK_SIZE) and y1 - y0 < 2 * BLOCK_SIZE:
            del self.segment_position[-1]
            self.grow_position((x1, y1 - BLOCK_SIZE))
            changes_occurred = True
        if (y1 + BLOCK_SIZE < y0 or y1 - y0 > 2 * BLOCK_SIZE) and y0 - y1 < 2 * BLOCK_SIZE:
            del self.segment_position[-1]
            self.grow_position((x1, y1 + BLOCK_SIZE))
            changes_occurred = True
        if (x1 + BLOCK_SIZE < x0 or x1 - x0 > 2 * BLOCK_SIZE) and x0 - x1 < 2 * BLOCK_SIZE:
            del self.segment_position[-1]
            self.grow_position((x1 + BLOCK_SIZE, y1))
            changes_occurred = True
        if (x1 - BLOCK_SIZE > x0 or x0 - x1 > 2 * BLOCK_SIZE) and x1 - x0 < 2 * BLOCK_SIZE:
            del self.segment_position[-1]
            self.grow_position((x1 - BLOCK_SIZE, y1))
            changes_occurred = True
        if changes_occurred:
            for i in range(0, len(self.segment_position)):
                x, y = self.segment_position[i]
                if y > WINDOW_HEIGHT:
                    y -= WINDOW_HEIGHT
                elif y < BLOCK_SIZE:
                    y += WINDOW_HEIGHT
                if x > WINDOW_WIDTH:
                    x -= WINDOW_WIDTH
                elif x < BLOCK_SIZE:
                    x += WINDOW_WIDTH
                self.segment_position[i] = (x, y)

    def grow(self, color=GREEN):
        """
        Lets grow the snake.

        :param color:
        """
        self.grow_color(color)
        self.grow_position()

    def grow_position(self, position=(0, 0)):
        """
        Adds a new position to the segment position's list.

        :param position:
        """
        x_pos, y_pos = position
        if x_pos == 0 and y_pos == 0:
            x_pos, y_pos = self.get_position_for_segments()
        self.segment_position = [(x_pos, y_pos)] + self.segment_position

    def grow_color(self, color=GREEN):
        """
        Adds a new color to the segment color's list.

        :param color:
        """
        self.segment_colors = self.segment_colors + [color]

    def get_position_for_segments(self) -> tuple:
        """
        Updated the positions of a segment.

        :return:
        """
        x, y = self.segment_position[0]
        if self.direction == 1:
            x += BLOCK_SIZE
        elif self.direction == 2:
            y += BLOCK_SIZE
        elif self.direction == 3:
            x -= BLOCK_SIZE
        else:
            y -= BLOCK_SIZE
        return x, y

    def check_for_collision(self) -> bool:
        """
        Checks if a collision occurred.

        :return:
        """
        collision = False
        x_check, y_check = self.segment_position[0]
        for i in range(3, len(self.segment_position)):
            x, y = self.segment_position[i]
            if Game.check_collision((x, y, BLOCK_SIZE, BLOCK_SIZE), (x_check, y_check, BLOCK_SIZE, BLOCK_SIZE)):
                collision = True
                break
        return collision


class Food:
    def __init__(self):
        """
        Initialized a Food object.
        """
        self.x_pos = randint(BLOCK_SIZE, WINDOW_WIDTH)
        self.y_pos = randint(BLOCK_SIZE, WINDOW_HEIGHT)
        color_index = randint(0, len(FOOD_COLORS) - 1)
        self.color = FOOD_COLORS[color_index]

    def draw(self, window):
        """
        Draws the Food object.

        :param window:
        """
        Game.draw_rect(window, self.x_pos, self.y_pos, self.color)


class Game:
    def __init__(self):
        """
        Initializes the Game object.
        """
        if SEGMENTS < 1:
            print('At least one segment is required')
            quit(1)
        self.is_paused = False
        self.score = 0
        self.time = float(0)
        self.main()

    @staticmethod
    def check_collision(rect0, rect1) -> bool:
        """
        Checks if a rectangle collided with an other.

        :param tuple rect0:
        :param tuple rect1:
        :return:
        """
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

    def check_food_collision(self, snake, food) -> bool:
        """
        Checks if the snake hit the food.

        :param Snake snake:
        :param Food food:
        :return:
        """
        x, y = snake.segment_position[0]
        if Game.check_collision((x, y, BLOCK_SIZE, BLOCK_SIZE),
                                (food.x_pos, food.y_pos, BLOCK_SIZE, BLOCK_SIZE)):
            snake.grow(food.color)

            food = Food()
            self.score += 1

        return snake, food

    def main(self):
        """
        Main game loop.
        """
        clock = pygame.time.Clock()
        window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        play = True
        game_over = False
        snake = Snake()
        food = Food()
        while play and not game_over:
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
                    if event.key in [pygame.K_SPACE, pygame.K_PAUSE]:
                        self.is_paused = not self.is_paused

            window.fill(BLACK)
            self.draw_score(window)
            self.draw_time(window)
            if not self.is_paused:
                snake.update_directions_if_necessary()
                snake, food = self.check_food_collision(snake, food)
                snake.move()
                self.time += 1 / FPS
                if snake.check_for_collision():
                    game_over = True
            food.draw(window)
            snake.draw(window)
            pygame.display.update()
        if game_over:
            while play:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        play = False

    @staticmethod
    def draw_rect(window, x, y, color=GREEN):
        """
        Draws a rectangle.

        :param window:
        :param int x:
        :param int y:
        :param tuple color:
        """
        pygame.draw.rect(window, color, (x, y, BLOCK_SIZE, BLOCK_SIZE))

    def draw_score(self, window):
        """
        Displays the score.

        :param window:
        """
        score_surface = font.render('Score: ' + str(self.score), False, RED)
        window.blit(score_surface, (0, 0))

    def draw_time(self, window):
        """
        Shows the time played.

        :param window:
        """
        hours = math.floor(self.time / 3600)
        minutes = math.floor(self.time / 60)
        seconds = math.floor(self.time % 60)
        time_surface = font.render('Time: ' + str(hours) + ':' + str(minutes) + ':' + str(seconds), False, RED)
        offset = math.floor((WINDOW_WIDTH - time_surface.get_width()) / 25) * 25
        window.blit(time_surface, (offset, 0))


# Start game
if __name__ == '__main__':
    game = Game()
    pygame.quit()
    quit()
