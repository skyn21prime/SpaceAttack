import pygame
from pygame.event import wait
from pygame.locals import QUIT
import random
import sys
 
# Initialize Pygame and set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption('Space Attack')
WIDTH, HEIGHT = DISPLAYSURF.get_size()
GAME_OVER_FONT = pygame.font.SysFont('sans', 100)
TITLE_FONT = pygame.font.SysFont('sans', 100)
SMAL_FONT = pygame.font.Font('Foldit-VariableFont_wght.ttf', 70)

BOX_FONT = pygame.font.Font('PixelifySans-VariableFont_wght.ttf', 40)

# Load and resize images
BOI_ORIG = pygame.image.load('Flying boi.png').convert_alpha()
ASTEROID_ORIG = pygame.image.load('Asteroid.png').convert_alpha()
BULLET_ORIG = pygame.image.load('Bullet.png').convert_alpha()

BOI = pygame.transform.scale(BOI_ORIG, (70, 70))
ASTEROID = pygame.transform.scale(ASTEROID_ORIG, (100, 100))
BULLET = pygame.transform.scale(BULLET_ORIG, (10, 20))

# Variables
player_img = BOI
player_x, player_y = WIDTH // 2, HEIGHT - 100
ASTEROID_SPEED = 2  # Smaller is faster
ASTEROID_COUNT = 9
Asteroids = [(random.randint(0, WIDTH), random.randint(-HEIGHT, 0))
             for _ in range(ASTEROID_COUNT)]
MAX_BULLETS = 10  # Maximum number of bullets allowed


player_rect = player_img.get_rect(center=(player_x, player_y)) # Center the player image to its collision box


# Title Screen
def show_title_screen():
    title_label = TITLE_FONT.render("Shoot the Asteroids!", 1, (255, 255, 255))
    start_label = SMAL_FONT.render("Press SPACEBAR to Start", 1, (255, 255, 30))

    while True:
        DISPLAYSURF.fill((0, 0, 0))
        DISPLAYSURF.blit(title_label, (WIDTH // 2 - title_label.get_width() // 2, HEIGHT // 3 - title_label.get_height() // 2))
        DISPLAYSURF.blit(start_label, (WIDTH // 2 - start_label.get_width() // 2, HEIGHT // 2 - start_label.get_height() // 2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

# Main loop
clock = pygame.time.Clock()
game_over = False
bullets = []  # Initialize bullets list

show_title_screen()

# Handle events
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    if not game_over:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and len(bullets) < MAX_BULLETS:
            bullets.append([player_x+27, player_y-10])

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 5
            player_img = pygame.transform.rotate(BOI, 5)
        elif keys[pygame.K_RIGHT] and player_x < WIDTH - player_img.get_width():
            player_x += 5
            player_img = pygame.transform.rotate(BOI, -5)
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 5
        if keys[pygame.K_DOWN] and player_y < HEIGHT - player_img.get_height():
            player_y += 5

    # Update bullets and Asteroids
    bullets = [[x, y - 5] for x, y in bullets if y > 0]
    Asteroids = [(x, y + ASTEROID_SPEED) if y < HEIGHT else (random.randint(0, WIDTH), 0) for x, y in Asteroids]
    player_rect = pygame.Rect(player_x, player_y, 50, 50)  # Create collision box for the player
  
    # Collision check: bullets and Asteroids
    for asteroid in Asteroids:
      asteroid_rect = pygame.Rect(asteroid[0], asteroid[1], 100, 100)  # Create collision box for each asteroid
      for bullet in bullets:
          bullet_rect = pygame.Rect(bullet[0], bullet[1], 10, 20)  # Create collision box for each bullet
          if bullet_rect.colliderect(asteroid_rect):
              bullets.remove(bullet)
              Asteroids.remove(asteroid)

    # Collision check: Flying boi and Asteroids
    for ax, ay in Asteroids:
        if player_x < ax < player_x + 50 and player_y < ay < player_y + 20:
            game_over = True
            break

    # Drawing
    DISPLAYSURF.fill((0, 0, 0))
    DISPLAYSURF.blit(player_img, (player_x, player_y))
    for ax, ay in Asteroids:
        DISPLAYSURF.blit(ASTEROID, (ax, ay))
    for bx, by in bullets:
        DISPLAYSURF.blit(BULLET, (bx, by))
    bullets_left = BOX_FONT.render(f"Bullets Enery: {MAX_BULLETS-len(bullets)}", 1, (255, 255, 255))
    DISPLAYSURF.blit(bullets_left, (10, 20)) # Display bullets left
    pygame.display.update()
   

    if game_over:
        game_over_label = GAME_OVER_FONT.render("Game Over", 1, (255, 0, 0))
        DISPLAYSURF.blit(game_over_label, (WIDTH // 2 - game_over_label.get_width() // 2, HEIGHT // 2 - game_over_label.get_height() // 2))
        pygame.display.update()
        time.sleep(2)
        show_title_screen()