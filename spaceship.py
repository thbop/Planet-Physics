from pyray import *
from vec2 import vec2

from body import Body

class Ship(Body):
    def __init__(self, pos, vel):
        super().__init__(pos, vel, 5, 1)

        self.color = Color(226, 108, 211, 255)

        self.thrust = .01
    
    def move(self):
        if is_key_down(KeyboardKey.KEY_KP_6): self.vel.x += self.thrust
        elif is_key_down(KeyboardKey.KEY_KP_4): self.vel.x -= self.thrust
        if is_key_down(KeyboardKey.KEY_KP_2): self.vel.y += self.thrust
        elif is_key_down(KeyboardKey.KEY_KP_8): self.vel.y -= self.thrust
