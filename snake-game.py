import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game for Browser 🐍")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Snake settings
BLOCK_SIZE = 10
SPEED = 10

# Font
font = pygame.font.SysFont("bahnschrift", 20)

# Function to show the score
def show_score(score):
    value = font.render(f"Score: {score}", True, WHITE)
    win.blit(value, [10, 10])

# Game function
def game():
    game_over = False
    game_close = False

    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake = []
    snake_length = 1

    food_x = random.randrange(0, WIDTH - BLOCK_SIZE, 10)
    food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, 10)

    clock = pygame.time.Clock()

    while not game_over:
        while game_close:
            win.fill(BLACK)
            msg = font.render("Game Over! Tap to Restart", True, RED)
            win.blit(msg, [WIDTH // 4, HEIGHT // 3])
            show_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    game()

        # Handle events (keyboard and touch)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change, y_change = -BLOCK_SIZE, 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change, y_change = BLOCK_SIZE, 0
                elif event.key == pygame.K_UP and y_change == 0:
                    x_change, y_change = 0, -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change, y_change = 0, BLOCK_SIZE

            # Touch controls for mobile
            elif event.type == pygame.FINGERDOWN:
                touch_x, touch_y = event.x * WIDTH, event.y * HEIGHT
                if touch_x < WIDTH // 3:
                    x_change, y_change = -BLOCK_SIZE, 0
                elif touch_x > WIDTH * 2 // 3:
                    x_change, y_change = BLOCK_SIZE, 0
                elif touch_y < HEIGHT // 3:
                    x_change, y_change = 0, -BLOCK_SIZE
                elif touch_y > HEIGHT * 2 // 3:
                    x_change, y_change = 0, BLOCK_SIZE

        # Move the snake
        x += x_change
        y += y_change

        # Check collisions with walls
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        win.fill(BLACK)
        pygame.draw.rect(win, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Snake body mechanics
        snake_head = [x, y]
        snake.append(snake_head)

        if len(snake) > snake_length:
            del snake[0]

        # Check self-collision
        for segment in snake[:-1]:
            if segment == snake_head:
                game_close = True

        for segment in snake:
            pygame.draw.rect(win, BLUE, [segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE])

        # Eating food
        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH - BLOCK_SIZE, 10)
            food_y = random.randrange(0, HEIGHT - BLOCK_SIZE, 10)
            snake_length += 1

        show_score(snake_length - 1)
        pygame.display.update()
        clock.tick(SPEED)

    pygame.quit()
    sys.exit()

# Run the game
game()