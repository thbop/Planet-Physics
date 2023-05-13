from pyray import *
from vec2 import vec2
import json

from body import *
from spaceship import Ship


class Game:
    def __init__(self):
        self.size = (1600, 900)

        init_window(self.size[0], self.size[1], 'Interplanetary Orbital Simulation')

        


        self.camera = Camera2D(
            Vector2(self.size[0] / 2, self.size[1] / 2),
            Vector2(self.size[0] / 2, self.size[1] / 2),
            0.0,
            1.0
        )
        self.camera_vel = Vector3(0, 0, 0)

        self.bodies = Bodies(self)

        self.ship = Ship(vec2(10, 10), vec2(0, 0))
        self.bodies.add(self.ship)

        self.load('thbop_sys.json')


        self.sel = {
            'sel': False,
            'pos': vec2(0, 0),
            'vel': vec2(0, 0)
        }


        self.fps = 60
        self.ffps = self.fps
        set_target_fps(self.fps)

    
    def click(self):
        if is_mouse_button_down(0):
            mouse = get_mouse_position()
            if not self.sel['sel']:
                self.sel['sel'] = True
                
                self.sel['pos'] = vec2(
                    mouse.x + self.camera.target.x - self.size[0] / 2,
                    mouse.y + self.camera.target.y - self.size[1] / 2
                    )
            else:
                self.sel['vel'] = vec2(
                    (mouse.x + self.camera.target.x - self.sel['pos'].x - self.size[0] / 2) / 50,
                    (mouse.y + self.camera.target.y - self.sel['pos'].y - self.size[1] / 2) / 50 
                    )
            draw_line_v(
                Vector2(
                    self.sel['pos'].x,
                    self.sel['pos'].y
                ),
                Vector2(
                    mouse.x + self.camera.target.x - self.size[0] / 2,
                    mouse.y + self.camera.target.y - self.size[1] / 2
                ),
                Color(100, 100, 100, 255)
            )

        elif self.sel['sel']:
            self.bodies.add( Planet(self.sel['pos'], self.sel['vel'], 10, 100 ) )
            self.sel = {
                'sel': False,
                'pos': vec2(0, 0),
                'vel': vec2(0, 0)
            }
        
    
    def load(self, filename):
        file = open(filename)
        data = json.load(file)
        file.close()

        for s in data['bodies']['stars']:
            star = Star(vec2(s['pos'][0], s['pos'][1]), vec2(s['vel'][0], s['vel'][1]), s['radius'], s['mass'])

            star.color = Color(s['color'][0], s['color'][1], s['color'][2], 255)
            star.flair_color = Color(s['flair-color'][0], s['flair-color'][1], s['flair-color'][2], 255)
            star.flair_amount = s['flair-amount']
            star.flair_range = s['flair-range']

            star.generate_flairs()

            self.bodies.add( star )
        for p in data['bodies']['planets']:
            self.bodies.add( Planet(vec2(p['pos'][0], p['pos'][1]), vec2(p['vel'][0], p['vel'][1]), p['radius'], p['mass']) )
    
    def move_camera(self):
        # Set some values
        move_acc = 1 / self.camera.zoom
        zoom_acc = .001

        move_cap = 4 / self.camera.zoom

        # Panning
        if is_key_down(KeyboardKey.KEY_D): self.camera_vel.x += move_acc
        elif is_key_down(KeyboardKey.KEY_A): self.camera_vel.x -= move_acc
        if is_key_down(KeyboardKey.KEY_S): self.camera_vel.y += move_acc
        elif is_key_down(KeyboardKey.KEY_W): self.camera_vel.y -= move_acc

        # Zooming
        if is_key_down(KeyboardKey.KEY_E): self.camera_vel.z += zoom_acc
        elif is_key_down(KeyboardKey.KEY_Q): self.camera_vel.z -= zoom_acc

        # Enforce panning velocity caps
        if self.camera_vel.x >= move_cap: self.camera_vel.x = move_cap
        elif self.camera_vel.x <= -move_cap: self.camera_vel.x = -move_cap
        if self.camera_vel.y >= move_cap: self.camera_vel.y = move_cap
        elif self.camera_vel.y <= -move_cap: self.camera_vel.y = -move_cap

        # Apply drag by damping
        self.camera_vel.x *= .95
        self.camera_vel.y *= .95
        self.camera_vel.z *= .95

        # Update camera position
        self.camera.target.x += self.camera_vel.x
        self.camera.target.y += self.camera_vel.y
        
        # Update camera zoom
        self.camera.zoom += self.camera_vel.z

        # Enforce zoom constraints
        if self.camera.zoom <= 0.05:
            self.camera.zoom = 0.05
            self.camera_vel.z = 0
        elif self.camera.zoom >= 7.0:
            self.camera.zoom = 7.0
            self.camera_vel.z = 0
    
    def display_stats(self):
        draw_text("Timestep: " + str(round(self.ffps)) + " : " + str(self.fps) + " : " + str(get_fps()), 10, 10, 20, GREEN)
        draw_text(f'''Ship:
    Position( {round(self.ship.pos.x, 1)}, {round(self.ship.pos.y, 1)} )
    Velocity( {round(self.ship.vel.x, 1)}, {round(self.ship.vel.y, 1)} )
        ''', 10, 40, 20, RED)
    

    def fps_controls(self):
        if is_key_down(KeyboardKey.KEY_RIGHT): self.ffps += 5
        elif is_key_down(KeyboardKey.KEY_LEFT): self.ffps -= 5

        if is_key_pressed(KeyboardKey.KEY_DOWN):
            self.fps = round(self.ffps)
            set_target_fps(self.fps)
        elif is_key_pressed(KeyboardKey.KEY_UP):
            self.fps = 60
            self.ffps = self.fps
            set_target_fps(self.fps)

    def run(self):
        while not window_should_close():

            self.move_camera()

            self.fps_controls()

            begin_drawing()
            clear_background(Color(0, 0, 0, 255))

            self.display_stats()

            begin_mode_2d(self.camera)
            


            # self.click()

            begin_blend_mode(BlendMode.BLEND_ADDITIVE)
            self.ship.move()
            self.bodies.run()
            end_blend_mode()

            end_mode_2d()
            
            end_drawing()
    
    def unload(self):
        close_window()



if __name__ == '__main__':
    game = Game()
    game.run()
    game.unload()