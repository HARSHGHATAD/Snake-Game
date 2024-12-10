import pygame
import random
import os

pygame.init()

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Game Window Dimensions
screen_width = 1500
screen_height = 800
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title and Icon
pygame.display.set_caption("Hungry Nagoba")
icon = pygame.image.load('snake_icon.png')  # Add your icon file (e.g., snake_icon.png)
pygame.display.set_icon(icon)

# Background Music
pygame.mixer.music.load('background_music.mp3')  # Add your music file (e.g., background_music.mp3)
pygame.mixer.music.play(-1)

# Game Sounds
eat_sound = pygame.mixer.Sound('eat.mp3')  # Add your sound file (e.g., eat.wav)
game_over_sound = pygame.mixer.Sound('game_over.mp3')

# Clock and Font
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 40)  # Use a custom font for better visuals

# Helper Functions
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, green, [x, y, snake_size, snake_size], border_radius=5)


def welcome():
    exit_game = False
    while not exit_game:
        # Welcome Screen Background
        gameWindow.fill(blue)
        text_screen("Welcome to Hungry Nagoba!", white, 450, 300)
        text_screen("Press Space Bar to Start", white, 490, 350)
        pygame.draw.rect(gameWindow, green, [700, 450, 120, 60], border_radius=20)
        text_screen("Play", black, 725, 460)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    Gameloop()

        pygame.display.update()
        clock.tick(50)

# Main Game Loop
def Gameloop():
    # Game Variables
    exit_game = False
    game_over = False
    snake_x = 100
    snake_y = 100
    velocity_x = 0
    velocity_y = 0
    init_velocity = 10
    food_x = random.randint(20, screen_width - 20)
    food_y = random.randint(20, screen_height - 20)
    score = 0
    snake_size = 20
    fps = 30

    # High Score Management
    if not os.path.exists("Bestscore.txt"):
        with open("Bestscore.txt", "w") as f:
            f.write("0")

    with open("Bestscore.txt", "r") as f:
        Bestscore = f.read()

    snk_list = []
    snk_length = 1

    while not exit_game:
        if game_over:
            pygame.mixer.music.stop()
            pygame.mixer.Sound.play(game_over_sound)

            with open("Bestscore.txt", "w") as f:
                f.write(str(Bestscore))

            gameWindow.fill(black)
            text_screen("Game Over! Press Enter to Restart", red, 400, 300)
            text_screen(f"Your Score: {score} Best Score: {Bestscore}", white, 400, 350)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.play(-1)  # Restart background music
                        Gameloop()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                # Handling Snake Movement
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = -init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_y = -init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x += velocity_x
            snake_y += velocity_y

            # Collision with Food
            if abs(snake_x - food_x) < 15 and abs(snake_y - food_y) < 15:
                score += 10
                food_x = random.randint(20, screen_width - 20)
                food_y = random.randint(20, screen_height - 20)
                snk_length += 5
                pygame.mixer.Sound.play(eat_sound)  # Play eat sound
                if score > int(Bestscore):
                    Bestscore = score

            # Update Game Window
            gameWindow.fill(black)
            text_screen(f"Score: {score} Best Score: {Bestscore}", white, 10, 10)
            pygame.draw.circle(gameWindow, red, (food_x, food_y), 10)  # Food as a circle
            head = [snake_x, snake_y]
            snk_list.append(head)
            if len(snk_list) > snk_length:
                del snk_list[0]

            # Game Over Conditions
            if head in snk_list[:-1] or snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True

            plot_snake(gameWindow, green, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

# Start Game
welcome()
