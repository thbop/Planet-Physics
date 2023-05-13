from pyray import *
from vec2 import vec2

from body import Body

class Ship(Body):
    def __init__(self, pos, vel, radius, mass):
        super().__init__(pos, vel, radius, mass)
        