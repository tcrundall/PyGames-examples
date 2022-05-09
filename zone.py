from matplotlib.pyplot import margins
import pygame

class Zone:
    """
    Defines a zone, e.g. for keeping
    objects within a region
    """
    margin = 10

    def __init__(self, left, top, width, height, image=None):
        self.rect = pygame.Rect(
            left + self.margin,
            top + self.margin,
            width - 2*self.margin,
            height - 2*self.margin,
        )
        self.contained_members = []
        self.free_members = []
        self.members = []
        self.image = image
    
    def add_contained_member(self, member):
        self.contained_members.append(member)

    def add_free_member(self, member):
        self.free_members.append(member)
    
    def update(self):
        for m in self.members:
            m.update()
        for m in self.contained_members:
            if not self.rect.contains(m.rect):
                m.rect.clamp_ip(self.rect)
            
        
        # As soon as free member leaves zone, delete member
        self.free_members = [m for m in self.free_members
            if self.rect.colliderect(m.rect)]

        self.members = self.contained_members + self.free_members
        
    
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.rect.left - self.margin, self.rect.top - self.margin))

        for m in self.members:
            m.draw(screen)
        

        
            

    

