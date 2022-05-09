import pygame
import numpy as np

KEYS = {
    1: {
        pygame.K_a : "LEFT",
        pygame.K_w : "UP",
        pygame.K_d : "RIGHT",
        pygame.K_s : "DOWN",
    },
    2: {
        pygame.K_LEFT : "LEFT",
        pygame.K_UP : "UP",
        pygame.K_RIGHT : "RIGHT",
        pygame.K_DOWN : "DOWN",
    },
}

DIREC = {
    1: 1,
    2: -1,
}

class Spaceship:
    width = 40
    height = 55
    speed = 5
    init_health = 10

    def __init__(self, x, y, color, player, image_file):
        self.vx = 0
        self.vy = 0
        self.color = color
        self.image = pygame.transform.scale(
            pygame.transform.rotate(
                image_file, DIREC[player] * 90,
            ),
            (self.width, self.height),
        )
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.health = self.init_health
        self.keys = KEYS[player]

    def __repr__(self):
        return "Spaceship %s %s"%(str(self.color), str(self.rect.center))

    def handle_control(self, keys_pressed):
        self.vx = 0
        self.vy = 0
        for key in self.keys:
            if keys_pressed[key]:
                if self.keys[key] == "LEFT":
                    self.vx -= 1
                elif self.keys[key] == "RIGHT":
                    self.vx += 1
                elif self.keys[key] == "UP":
                    self.vy -= 1
                elif self.keys[key] == "DOWN":
                    self.vy += 1


    def update(self):
        if self.vx or self.vy:
            vel_vec = np.array([self.vx, self.vy])
            vel_vec = self.speed * vel_vec / np.linalg.norm(vel_vec)
            self.rect.move_ip(*vel_vec)


    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
