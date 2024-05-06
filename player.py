
import math
import pygame as pg
from config import *

class Player:
    def __init__(self, app) -> None:
        self.app = app

        self.pos = pg.Vector2(0, 0)
        self.vel = pg.Vector2(0, 0)
        
        self.hand_pos = pg.Vector2(0, 0)
        self.hand_target = pg.Vector2(0, 0)
        self.hand_vel = pg.Vector2(0, 0)
        self.hand_state = 'ready'
        self.push_vel = pg.Vector2(0, 0)
        self.attached = False
        self.player_target = pg.Vector2(0, 0)

        self.surf = pg.Surface((80, 100))
        self.surf.fill(PLAYER_COL)
        self.rect = self.surf.get_rect(center = self.pos)

    def update(self):
        self.starting_hand_pos = self.hand_pos.copy()
        # Hand movement
        if self.app.mouse[0]:
            self.hand_pos = self.pos.copy()
            self.hand_state = 'thrown'

        if self.app.mouse_pressed[0]:
            self.hand_target = (self.app.mouse_pos - self.app.screen_off + self.app.world_position) 
        else:
            self.hand_target = self.pos.copy()
            
        if self.hand_state == 'thrown':
            
            self.hand_vel = self.calc_movement_vector(self.hand_pos, self.hand_target)

            if self.hand_pos.distance_to(self.hand_target) <= self.hand_vel.length():
                self.hand_pos = self.hand_target.copy()
                
                if self.is_hand_attached() and self.hand_pos != self.pos: # put these other conditions in the function
                    self.hand_state = 'attached'
                    self.vel = pg.Vector2(0, 0)
                    self.player_target = self.pos.copy()
                    
                if self.hand_pos == self.pos:
                    self.hand_state = 'ready'

            else:
                self.hand_pos += self.hand_vel

        # Gravity
        self.gravity = pg.Vector2(0, 0)
        # Player movement
        if self.hand_state == 'attached':
            self.player_target -= self.app.mouse_vel  
            self.hand_vel = self.calc_movement_vector(self.pos, self.player_target)
            self.pos += self.hand_vel
            
            if self.pos.distance_to(self.player_target) <= self.hand_vel.length():
                self.pos = self.player_target.copy()

            if not self.app.mouse_pressed[0]:
                self.hand_state = 'thrown'
                self.vel = self.hand_vel
      

        self.vel += self.gravity * self.app.dt
        #self.total_force = self.gravity + self.spring_force
        #self.vel += self.total_force * self.app.dt/ MASS
        # Add velocity
        self.pos += self.vel
        self.hand_pos += self.vel
        self.rect.center = self.pos

    def is_hand_attached(self):

        return True

    def calc_movement_vector(self, origin, desination):
       
        vel = pg.Vector2(0, 0)

        displacement_to_target = (desination - origin)
        distance_to_target = displacement_to_target.length()
            
        if distance_to_target != 0:
            if distance_to_target >= HAND_DISTANCE_DROPOFF:
                distance_to_target = 1
            else:
                distance_to_target /= HAND_DISTANCE_DROPOFF
            
            vel = displacement_to_target.normalize()
            vel *= HAND_SPEED * (math.cos((1 - distance_to_target) * 1.3)) # add delta time

        return vel

    def render(self):
        # Here so rendering is fixed find better method

        if self.app.mouse_pressed[0]:
            self.hand_target = (self.app.mouse_pos - self.app.screen_off + self.app.world_position) 
        else:

            self.hand_target = self.pos.copy()
        # Body
        render_rect = pg.Rect(0, 0, self.rect.width, self.rect.height) 
        render_rect.center = (self.pos + self.app.screen_off - self.app.world_position)
        self.app.screen.blit(self.surf, render_rect)

        # Hand target
        pg.draw.circle(self.app.screen, BLACK, self.hand_target + self.app.screen_off - self.app.world_position, 10)

        # Hand
        pg.draw.circle(self.app.screen, RED, self.hand_pos + self.app.screen_off - self.app.world_position, 10)

        # Player target
        pg.draw.circle(self.app.screen, (0, 255, 0), self.player_target + self.app.screen_off - self.app.world_position, 10)



# after code refactor - 
# determine a target for the player position
# use the same code for the hand movement to determine a counter force to get to the target
# then add on the gravity force and air resistance
# which means the other vels and stuff need to be turned into a force
# that should give a good movement system






