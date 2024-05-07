

import pygame as pg
import sys

from config import *
from player import *

class Game:
    def __init__(self) -> None:
        # Initialize pygame
        pg.init()
        self.clock = pg.time.Clock()
        
        self.screen = pg.display.set_mode(WINDOW_SIZE)
        self.running = True

        self.dt = 0.0

    def new_game(self):
        self.screen_off = pg.Vector2(WINDOW_SIZE[0]/2, WINDOW_SIZE[1]/2)
        self.world_position = pg.Vector2(0, 0)

        self.player = Player(self)

        self.mouse_pressed = [False] * 5
        self.count = 0
        self.old_mouse_pos = pg.Vector2(0, 0)


    def events(self):
        
        self.mouse = [False] * 5
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    self.mouse[0] = True
                    self.mouse_pressed[0] = True
            if event.type == pg.MOUSEBUTTONUP:
                if event.button == pg.BUTTON_LEFT:
                    self.mouse_pressed[0] = False


        self.mouse_pos = pg.Vector2(pg.mouse.get_pos())
        self.mouse_vel = pg.Vector2(self.mouse_pos - self.old_mouse_pos)
        self.keys = pg.key.get_pressed()

        self.old_mouse_pos = self.mouse_pos.copy()



    def update(self):
        
        self.player.update()
        self.world_position = self.player.pos.copy()

    def render(self):
        self.screen.fill(BACKGROUND_COL)

        self.player.render()

        for y in range(0, WINDOW_SIZE[1], 100):
            pg.draw.line(self.screen, BLACK, (0, y-self.world_position.y % 100), (WINDOW_SIZE[0], y-self.world_position.y % 100))
            
            #pg.draw.line(self.screen, WHITE, (0, (y-self.world_position.y % 100)+50), (WINDOW_SIZE[0], (y-self.world_position.y % 100)+50))
        for x in range(0, WINDOW_SIZE[0], 100):
            pg.draw.line(self.screen, BLACK, (x-self.world_position.x % 100, 0), (x-self.world_position.x % 100, WINDOW_SIZE[1]))
            #pg.draw.line(self.screen, WHITE, ((x-self.world_position.x % 100)+50, 0), ((x-self.world_position.x % 100)+50, WINDOW_SIZE[1]))


    def debug(self):
        pass

if __name__ == '__main__':
   Engine = Game()
   Engine.new_game()

   while Engine.running:

       Engine.events()
       Engine.update()
       Engine.render()

       Engine.dt = Engine.clock.tick(FPS)/1000
       pg.display.flip()

pg.quit()
sys.exit()


# make it so a thing that activates the python venv runs everytime the python lsp attachs
