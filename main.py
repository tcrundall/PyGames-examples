import pygame
import os
from bullet import Bullet
from spaceship import Spaceship
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

BORDER_WIDTH = 10
BORDER = pygame.Rect(WIDTH//2 - BORDER_WIDTH//2, 0, BORDER_WIDTH, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
GAME_STATUS_FONT = pygame.font.SysFont("Comicsans", 60)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 55
BULLET_WIDTH, BULLET_HEIGHT = 15, 3

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
# YELLOW_SPACESHIP_IMAGE = os.path.join("Assets", "spaceship_yellow.png")

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_yellow.png'))
# YELLOW_SPACESHIP = pygame.transform.scale(pygame.transform.rotate(
#     YELLOW_SPACESHIP_IMAGE, 90), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('Assets','spaceship_red.png'))
RED_SPACESHIP = pygame.transform.scale(pygame.transform.rotate(
        RED_SPACESHIP_IMAGE, 270), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),
    (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, game_status, winner_text):
    WIN.blit(SPACE, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red.health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow.health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    for b in yellow_bullets:
        b.draw()
        # pygame.draw.rect(WIN, YELLOW, b)
    for b in red_bullets:
        b.draw()
        # pygame.draw.rect(WIN, RED, b)
    red.draw(WIN)
    yellow.draw(WIN)
    # WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    # WIN.blit(RED_SPACESHIP, (red.x, red.y))

    game_status_text = None
    if game_status == "finished":
        game_status_text = GAME_STATUS_FONT.render(winner_text, 1, WHITE)
    elif game_status == "paused":
        game_status_text = GAME_STATUS_FONT.render("Paused", 1, WHITE)
    
    if game_status_text:
        WIN.blit(game_status_text, (WIDTH//2, HEIGHT//2))

    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    # Yellow
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT: # DOWN
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    # Red
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:    # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # DOWN
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x + BULLET_WIDTH < 0:
            red_bullets.remove(bullet)


def main():
    yellow = Spaceship(200, 300, YELLOW, 1, YELLOW_SPACESHIP_IMAGE)
    red = Spaceship(700, 300, RED, 2, RED_SPACESHIP_IMAGE)

    yellow_bullets = []
    red_bullets = []

    clock = pygame.time.Clock()
    run = True
    game_status = "playing" # "paused", "finished"
    
    while run:
        clock.tick(FPS)
        # --------------------------------------------------
        # ---- Handle instant events (key downs etc.) ------
        # --------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_status == "playing": 
                if event.type == RED_HIT:
                    red.health -= 1
                    BULLET_HIT_SOUND.play()
                
                if event.type == YELLOW_HIT:
                    yellow.health -= 1
                    BULLET_HIT_SOUND.play()

                if event.type == pygame.KEYDOWN and len(yellow_bullets) < MAX_BULLETS:
                    if event.key == pygame.K_LSHIFT and len(yellow_bullets) < MAX_BULLETS:
                        bullet = Bullet(
                            YELLOW,
                            x=yellow.rect.x + yellow.rect.width,
                            y=yellow.rect.y + yellow.rect.height//2 - Bullet.height//2,
                            direc=1,
                            screen=WIN
                            )
                        # bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    
                    if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                        bullet = Bullet(
                            RED,
                            x=red.rect.x - Bullet.width,
                            y=red.rect.y + red.rect.height//2 - Bullet.height//2,
                            direc=-1,
                            screen=WIN
                            )
                        # bullet = pygame.Rect(red.x - 10, red.y + red.height//2 - 2, 10, 5)
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
                    
                    if event.key == pygame.K_SPACE:
                        game_status = "paused"


            elif game_status == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_status = "playing"
            elif game_status == "finished":
                pass
        
        # --------------------------------------------------
        # ---- Handle continuousevents (holding keys) ------
        # --------------------------------------------------
        keys_pressed = pygame.key.get_pressed()
        yellow.handle_control(keys_pressed)
        red.handle_control(keys_pressed)
        
        # --------------------------------------------------
        # ---- Handle internal game logic ------------------
        # --------------------------------------------------
        if game_status == "playing":
            for b in yellow_bullets:
                b.update()
            for b in red_bullets:
                b.update()
            yellow.update()
            red.update()

        # --------------------------------------------------
        # ---- Handle game state changes -------------------
        # --------------------------------------------------
        winner_text = ""
        if red.health <= 0:
            winner_text = "Yellow Wins!"

        if yellow.health <= 0:
            winner_text = "Red Wins!"
                
        if winner_text:
            game_status = "finished"


        # --------------------------------------------------
        # ---- Draw game state -----------------------------
        # --------------------------------------------------
        draw_window(red, yellow, red_bullets, yellow_bullets, game_status, winner_text) 

    pygame.quit()

if __name__ == "__main__":
    main()