import pygame
from pygame.math import Vector2 as vec2
import json

from body import Bodies

pygame.init()

class Game:
    def __init__(self):
        self.size = (1600, 900)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Planet Physics')

        self.line_surf = pygame.Surface(self.size)

        self.bodies = Bodies(self)

        self.load('solar_system.json')

        self.sel = {
            'sel': False,
            'pos': vec2(0, 0),
            'vel': vec2(0, 0)
        }

    
    def click(self):
        
        if pygame.mouse.get_pressed()[0]:
            mx, my = pygame.mouse.get_pos()
            if not self.sel['sel']:
                self.sel['sel'] = True
                
                self.sel['pos'] = vec2(mx, my)
            else:
                self.sel['vel'] = vec2(
                    (mx - self.sel['pos'].x) / 50,
                    (my - self.sel['pos'].y) / 50
                    )
            pygame.draw.line(self.screen, (100, 100, 100), self.sel['pos'], (mx, my), 3)    

        elif self.sel['sel']:
            self.bodies.add( self.sel['pos'], self.sel['vel'], 10, 100 )
            self.sel = {
                'sel': False,
                'pos': vec2(0, 0),
                'vel': vec2(0, 0)
            }
        
    
    def load(self, filename):
        file = open(filename)
        data = json.load(file)
        file.close()

        for b in data['bodies']:
            self.bodies.add( vec2(b['pos'][0], b['pos'][1]), vec2(b['vel'][0], b['vel'][1]), b['radius'], b['mass'] )
    

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            

            self.screen.fill((0, 0, 0))

            self.screen.blit(self.line_surf, (0, 0))

            self.line_surf.fill((1, 1, 1), special_flags=pygame.BLEND_SUB)


            self.click()

            self.bodies.run()

            clock.tick(60)
            pygame.display.flip()

if __name__ == '__main__':
    game = Game()
    game.run()