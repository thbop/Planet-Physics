from pyray import *
from random import randint, uniform

from vec2 import vec2
from body import Body

class Particle:
    def __init__(self, pos, vel, radius):
        self.pos = pos
        self.vel = vel
        self.radius = radius

        self.timer = randint(30, 70)

class Ship(Body):
    def __init__(self, pos, vel):
        super().__init__(pos, vel, 5, 1)

        self.color = Color(226, 108, 211, 255)

        self.particles = []

        self.thrust = .01
    
    def move(self):
        m = {'right': False, 'left': False, 'down': False, 'up': False}

        if is_key_down(KeyboardKey.KEY_KP_6):
            m['right'] = True

        elif is_key_down(KeyboardKey.KEY_KP_4):
            m['left'] = True

        if is_key_down(KeyboardKey.KEY_KP_2):
            m['down'] = True

        elif is_key_down(KeyboardKey.KEY_KP_8):
            m['up'] = True
        
        if is_key_down(KeyboardKey.KEY_KP_5):
            if self.vel.x > 0: m['left'] = True
            else: m['right'] = True
            if self.vel.y > 0: m['up'] = True
            else: m['down'] = True

        if m['right']:
            self.vel.x += self.thrust
            self.add_p(self.pos.copy(), vec2(-1, uniform(-.1, .1)), randint(1, 2))
        elif m['left']:
            self.vel.x -= self.thrust
            self.add_p(self.pos.copy(), vec2(1, uniform(-.1, .1)), randint(1, 2))
        if m['down']:
            self.vel.y += self.thrust
            self.add_p(self.pos.copy(), vec2(uniform(-.1, .1), -1), randint(1, 2))
        elif m['up']:
            self.vel.y -= self.thrust
            self.add_p(self.pos.copy(), vec2(uniform(-.1, .1), 1), randint(1, 2))

    
    def add_p(self, pos, vel, radius):
        self.particles.append(Particle(pos, vel, radius))
    
    def run_p(self):
        remove_list = []
        for p in self.particles:
            p.pos += p.vel

            p.timer -= 1
            if p.timer <= 0:
                remove_list.append(p)
            
            draw_circle_v(p.pos.toray(), p.radius, Color(100, 140, 200, 255))
        
        for p in remove_list: self.particles.remove(p)
