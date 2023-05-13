import pygame
import pygame.freetype



class Gui:
    def __init__(self, gm):
        self.gm = gm
        self.mouse_down = False

        self.font_size = 15
        self.font = pygame.freetype.SysFont('Arial', self.font_size)

        self.dropdown_file = False
        self.dropdown_edit = False
        
    
    def _button(self, rect, text, onclick=None, onhover=None):
        if rect.collidepoint(self.mouse):
            pygame.draw.rect(self.gm.screen, (200, 200, 200), rect, 1, 2)

            if onhover != None:
                onhover()

            if pygame.mouse.get_pressed()[0] and not self.mouse_down:
                self.mouse_down = True
                if onclick != None:
                    onclick()

            elif not pygame.mouse.get_pressed()[0] and self.mouse_down:
                self.mouse_down = False
        else:
            pygame.draw.rect(self.gm.screen, (150, 150, 150), rect, 1, 2)
        
        self.font.render_to(self.gm.screen, [
                rect.centerx - ( len(text) * (self.font_size / 2) ) / 2,
                rect.centery - ( self.font_size / 2 ),
                0, 0
            ], text, (255, 255, 255))
    
    def _dropdown_file(self):
        self._button(pygame.Rect(5, 5, 70, 20), 'File', onhover=self._dropdown_file_update)
        if self.dropdown_file:
            self._button(pygame.Rect(5, 30, 70, 20), 'Save')
            self._button(pygame.Rect(5, 55, 70, 20), 'Open')

    def _dropdown_file_update(self):
        self.dropdown_file = True
    
    def _dropdown_edit(self):
        self._button(pygame.Rect(90, 5, 70, 20), 'Edit', onhover=self._dropdown_edit_update)
        if self.dropdown_edit:
            self._button(pygame.Rect(90, 30, 70, 20), 'Trails')
            self._button(pygame.Rect(90, 55, 70, 20), 'Turbo')

    def _dropdown_edit_update(self):
        self.dropdown_edit = True

    def _close_dropdowns(self):
        if pygame.mouse.get_pressed()[0]:
            self.dropdown_file = False
            self.dropdown_edit = False

        
    
    def run(self):
        self.mouse = pygame.mouse.get_pos()

        self._dropdown_file()
        self._dropdown_edit()


        self._close_dropdowns()
        # self._button(pygame.Rect(10, 10, 100, 30), 'Test Button')
