from pyray import *
from vec2 import vec2

from random import randint



class Body:
    def __init__(self, pos, vel, radius, mass):
        self.pos = pos
        self.vel = vel
        self.acc = vec2(0, 0)

        self.radius = radius
        self.mass = mass

    def _generate_color(self):
        self.color = Color(
            randint(150, 255), randint(150, 255), randint(150, 255), 255
        )

    
    def collide(self, other):
        if self.radius + other.radius >= self.pos.distance_to(other.pos):
            return True
        else:
            return False
    
    def render(self):
        draw_circle_v(self.pos.toray(), self.radius, self.color)

class Planet(Body):
    def __init__(self, pos, vel, radius, mass):
        super().__init__(pos, vel, radius, mass)
        self._generate_color()


class Star(Body):
    def __init__(self, pos, vel, radius, mass):
        super().__init__(pos, vel, radius, mass)

        self.flair_color = Color(5, 5, 5, 255)
        self.flair_amount = 250
        self.flair_range = 30

        self.flairs = []
    
    def generate_flairs(self):
        for i in range(self.flair_amount):
            self.flairs.append(
                Vector3(
                    randint(-self.flair_range, self.flair_range),
                    randint(-self.flair_range, self.flair_range),
                    randint(self.radius - self.flair_range, self.radius + self.flair_range)
                )
            )
    
    def render(self):
        draw_circle_v(self.pos.toray(), self.radius, Color(200, 200, 200, 255))
        for f in self.flairs:
            draw_circle_gradient(int(f.x + self.pos.x), int(f.y + self.pos.y), int(f.z), self.flair_color, Color(0, 0, 0, 255))
    


class Bodies:
    def __init__(self, gm):
        self.gm = gm

        self.bodies = []

        self.g = .01
    
    def add(self, body):
        self.bodies.append( body )
    
    
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

                    b.acc = vec2(
                        -( self.g * b2.mass * dir_n.x ) / dir_m**2,
                        -( self.g * b2.mass * dir_n.y ) / dir_m**2
                    )

                    b.vel += b.acc

                    # Check collision
                    both_star = ( isinstance(b, Star) and isinstance(b2, Star) )
                    b2_not_star = not isinstance(b2, Star)
                    if b.collide(b2) and ( b2_not_star or both_star ):
                        b.pos = vec2(
                            ( b.pos.x + b2.pos.x ) / 2,
                            ( b.pos.y + b2.pos.y ) / 2
                        )

                        b.vel = vec2(
                            ( b.mass * b.vel.x + b2.mass * b2.vel.x ) / ( b.mass + b2.mass ),
                            ( b.mass * b.vel.y + b2.mass * b2.vel.y ) / ( b.mass + b2.mass )
                        )

                        b.radius += int(b2.radius / 2)
                        b.mass += b2.mass

                        if both_star:
                            b.flairs = []
                            b.flair_amount += int(b2.flair_amount / 2)
                            b.flair_range += int(b2.flair_range / 2)
                            b.generate_flairs()

                            b.flair_color.r = int((b.flair_color.r + b2.flair_color.r) / 2)
                            b.flair_color.g = int((b.flair_color.g + b2.flair_color.g) / 2)
                            b.flair_color.b = int((b.flair_color.b + b2.flair_color.b) / 2)


                        # Remove b2
                        self.bodies.remove( b2 )

            # Update position
            b.pos += b.vel


            # Draw
            b.render()

