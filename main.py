import pygame
import os
from bullet import Bullet
from spaceship import Spaceship
from zone import Zone
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

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_yellow.png'))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets','spaceship_red.png'))

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')),
    (WIDTH, HEIGHT))


def draw_window(red, yellow, zones, game_status, winner_text):
    for zone in zones:
        zone.draw(WIN)

    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red.health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow.health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    game_status_text = None
    if game_status == "finished":
        game_status_text = GAME_STATUS_FONT.render(winner_text, 1, WHITE)
    elif game_status == "paused":
        game_status_text = GAME_STATUS_FONT.render("Paused", 1, WHITE)
    
    if game_status_text:
        WIN.blit(game_status_text, (
            WIDTH//2 - game_status_text.get_width()//2,
            HEIGHT//2 - game_status_text.get_height()//2
            ))

    pygame.display.update()


def init_game_zones():
    zones = []

    game_zone = Zone(0, 0, WIDTH, HEIGHT, image=SPACE)
    zones.append(game_zone)

    yellow = Spaceship(200, HEIGHT//2, YELLOW, 1, YELLOW_SPACESHIP_IMAGE)
    yellow_zone = Zone(left=0, top=0, width=WIDTH//2, height=HEIGHT)
    yellow_zone.add_contained_member(yellow)
    zones.append(yellow_zone)

    red = Spaceship(WIDTH - 200, HEIGHT//2, RED, 2, RED_SPACESHIP_IMAGE)
    red_zone = Zone(left=WIDTH//2, top=0, width=WIDTH//2, height=HEIGHT)
    red_zone.add_contained_member(red)
    zones.append(red_zone)

    return yellow, red, game_zone, zones


def main():
    yellow, red, game_zone, zones = init_game_zones()

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
                n_yellow_bullets = len([b for b in game_zone.free_members if b.color == YELLOW])
                n_red_bullets = len([b for b in game_zone.free_members if b.color == RED])

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LSHIFT and n_yellow_bullets < MAX_BULLETS:
                        bullet = Bullet(
                            YELLOW,
                            x=yellow.rect.x + yellow.rect.width,
                            y=yellow.rect.y + yellow.rect.height//2 - Bullet.height//2,
                            direc=1,
                            )
                        game_zone.add_free_member(bullet)
                        BULLET_FIRE_SOUND.play()
                    
                    if event.key == pygame.K_RSHIFT and n_red_bullets < MAX_BULLETS:
                        bullet = Bullet(
                            RED,
                            x=red.rect.x - Bullet.width,
                            y=red.rect.y + red.rect.height//2 - Bullet.height//2,
                            direc=-1,
                            )
                        game_zone.add_free_member(bullet)
                        BULLET_FIRE_SOUND.play()
                    
                    if event.key == pygame.K_SPACE:
                        game_status = "paused"


            elif game_status == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_status = "playing"
            elif game_status == "finished":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    yellow, red, game_zone, zones = init_game_zones()
                    game_status = "playing" 

        
        # --------------------------------------------------
        # ---- Handle continuous events (holding keys) -----
        # --------------------------------------------------
        keys_pressed = pygame.key.get_pressed()
        yellow.handle_control(keys_pressed)
        red.handle_control(keys_pressed)
        
        # --------------------------------------------------
        # ---- Handle internal game logic ------------------
        # --------------------------------------------------
        if game_status == "playing":
            for z in zones:
                z.update()
            
            for b in game_zone.free_members[:]:
                if b.color == YELLOW:
                    if red.rect.colliderect(b.rect):
                        red.health -= 1
                        BULLET_HIT_SOUND.play()
                        game_zone.free_members.remove(b)
                if b.color == RED:
                    if yellow.rect.colliderect(b.rect):
                        yellow.health -= 1
                        BULLET_HIT_SOUND.play()
                        game_zone.free_members.remove(b)

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
        draw_window(red, yellow, zones, game_status, winner_text) 

    pygame.quit()

if __name__ == "__main__":
    main()