import pygame

class Bullet():
    width = 15
    height = 3
    velx = 10

    def __init__(self, color, x, y, direc, screen):
        self.color = color
        self.screen = screen
        self.direc = direc
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self):
        # update position based on velocity
        self.rect.x += self.direc * self.velx

        # check for collision
        # - maybe this can be handled by spaceships?

        # check for leaving game boundary?
        # - maybe this can be handled by 'GameRect'

    def draw(self):
        pygame.draw.rect(self.screen, self.color, self.rect)        
