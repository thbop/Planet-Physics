import pygame
from pygame.math import Vector2 as vec2

from random import randint



class Body:
    def __init__(self, pos, vel, radius, mass):
        self.pos = pos
        self.vel = vel

        self.radius = radius
        self.mass = mass

        self.color = (
            randint(150, 255), randint(150, 255), randint(150, 255)
        )

    
    def collide(self, other):
        if self.radius + other.radius >= self.pos.distance_to(other.pos):
            return True
        else:
            return False
    


class Bodies:
    def __init__(self, gm):
        self.gm = gm

        self.bodies = []

        self.g = .01
    
    def add(self, pos, vel, radius, mass):
        self.bodies.append( Body(pos, vel, radius, mass) )
    
    def run(self):
        for b in self.bodies:
            for b2 in self.bodies:
                if b2 != b:
                    # Distance
                    dis = b.pos.distance_to(b2.pos)

                    # Direction
                    direction = b.pos - b2.pos
                    dir_n = direction.normalize()
                    dir_m = direction.magnitude()

                    acc = vec2(
                        -( self.g * b2.mass * dir_n.x ) / dir_m**2,
                        -( self.g * b2.mass * dir_n.y ) / dir_m**2
                    )

                    b.vel += acc

                    # Check collision
                    if b.collide(b2):
                        b.pos = vec2(
                            ( b.pos.x + b2.pos.x ) / 2,
                            ( b.pos.y + b2.pos.y ) / 2
                        )

                        b.vel = vec2(
                            ( b.mass * b.vel.x + b2.mass * b2.vel.x ) / ( b.mass + b2.mass ),
                            ( b.mass * b.vel.y + b2.mass * b2.vel.y ) / ( b.mass + b2.mass )
                        )

                        b.radius += b2.radius / 2
                        b.mass += b2.mass


                        # Remove b2
                        self.bodies.remove( b2 )

            # Update position
            b.pos += b.vel


            # Draw
            pygame.draw.circle(self.gm.screen, b.color, [b.pos.x - self.gm.camera.rect.x, b.pos.y - self.gm.camera.rect.y], b.radius, 0)

            # Draw trail
            fade = 50
            pygame.draw.circle(self.gm.line_surf,
                               (b.color[0] - fade, b.color[1] - fade, b.color[2] - fade ), # Fade color
                               [b.pos.x - self.gm.camera.rect.x, b.pos.y - self.gm.camera.rect.y], # Adjust for camera
                               2, 0)