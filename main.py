import math
import pygame
import time
import random

# defining the font size from Pygame
pygame.font.init()


# Setting up dimensions for the main window of the game
WIDTH, HEIGHT = 1000, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Main window title
pygame.display.set_caption("Space Dodge")

# Placing a background image into a variable and scaling it to fit the size of the main window
BG = pygame.transform.scale(pygame.image.load("bg.jpg"), (WIDTH, HEIGHT))

# Setting players dimensions
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VEL = 5

# Setting dimensions for obstacles
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 3

# Setting the font for displaying the time
FONT = pygame.font.SysFont("arial", 30)


def draw(player, time_passed, stars):
    """
    Placing images, text and player to the main window
    @param player: Main player icon
    @param time_passed: Elapsed Time
    @param stars: Stars to be drawn
    """

    WIN.blit(BG, (0, 0))

    # Our text settings
    time_text = FONT.render(f"Time: {math.floor(time_passed)}s", True, "yellow")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    # Placing star on the main window
    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()


def main():
    """
    Runs the main logic of the game
    """

    run = True

    # Setting the main values for the player
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    # Creating condition for speed movement of the player
    clock = pygame.time.Clock()

    # Starting time from which we will count the elapsed time
    start_time = time.time()

    # We set value which will be measured in milliseconds
    star_add_increment = 2000
    star_count = 0

    # An array for collecting obstacles
    stars = []
    hit = False

    while run:
        # Setting the FPS of the player and increasing the "star_count" which represent milliseconds
        star_count += clock.tick(60)

        # Calculating the elapsed time
        elapsed_time = time.time() - start_time

        # Checking if "star_count" milliseconds reaching initial set up of milliseconds
        if star_count > star_add_increment:

            # Number 3 is default obstacles that we start the game
            for _ in range(3):

                # Choosing random x position for our obstacle
                star_x = random.randint(0, WIDTH - STAR_WIDTH)

                # Setting the boundaries of our obstacle
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            # With this statement we can not go below 200 milliseconds
            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        # Checking if we close the window with "X" button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Checking for specific pressed key from the keyboard
        # and moving the player in the desired direction
        keys = pygame.key.get_pressed()

        # We define boundaries between where the player can move
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + player.width + PLAYER_VEL <= WIDTH:
            player.x += PLAYER_VEL

        # Iterating trough each obstacle, moving its position to the bottom of the screen
        # and checking if the obstacles collides with the player
        for star in stars[:]:
            star.y += STAR_VEL

            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        # Special condition to show that we lost the game if we obstacle hit the player
        if hit:
            lost_text = FONT.render("You Lost!", True, "#09e686")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    main()
