import pygame
from pygame.locals import *

class Camera:
    def __init__(self, size):
        self.rect = pygame.Rect(0, 0, size[0], size[1])
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = 1
        self.vel_cap = 4
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_d]:
            self.vel.x += self.acc
        if keys[K_a]:
            self.vel.x -= self.acc
        if keys[K_s]:
            self.vel.y += self.acc
        if keys[K_w]:
            self.vel.y -= self.acc
        
        if self.vel.x >= self.vel_cap: self.vel.x = self.vel_cap
        elif self.vel.x <= -self.vel_cap: self.vel.x = -self.vel_cap
        if self.vel.y >= self.vel_cap: self.vel.y = self.vel_cap
        elif self.vel.y <= -self.vel_cap: self.vel.y = -self.vel_cap

        self.vel *= .98
        self.rect.x += self.vel.x
        self.rect.y += self.vel.y