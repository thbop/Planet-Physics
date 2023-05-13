from pyray import *
from vec2 import vec2
import json

from body import Bodies


class Game:
    def __init__(self):
        self.size = (1600, 900)

        init_window(self.size[0], self.size[1], 'Interplanetary Orbital Simulation')

        set_target_fps(60)

        self.line_surf = load_render_texture(self.size[0], self.size[1])

        self.camera = Camera2D(
            Vector2(self.size[0] / 2, self.size[1] / 2),
            Vector2(self.size[0] / 2, self.size[1] / 2),
            0.0,
            1.0
        )
        self.camera_vel = Vector3(0, 0, 0)

        self.bodies = Bodies(self)

        self.load('solar_system.json')

        self.sel = {
            'sel': False,
            'pos': vec2(0, 0),
            'vel': vec2(0, 0)
        }

    
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
    
    def move_camera(self):
        # Set some constants
        move_acc = 1
        zoom_acc = .001

        move_cap = 4

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
    

    def run(self):
        while not window_should_close():
            

            self.move_camera()

            begin_drawing()
            begin_mode_2d(self.camera)
            clear_background(Color(0, 0, 0, 255))

            # self.screen.blit(self.line_surf, (0, 0))
            # self.line_surf.fill((1, 1, 1), special_flags=pygame.BLEND_SUB)


            self.click()

            self.bodies.run()

            draw_texture(self.line_surf.texture, 0, 0, WHITE)
            end_mode_2d()
            
            end_drawing()
    
    def unload(self):
        unload_render_texture(self.line_surf)
        close_window()



if __name__ == '__main__':
    game = Game()
    game.run()
    game.unload()