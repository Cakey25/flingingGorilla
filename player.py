
import math
import pygame as pg
from pygame.math import Vector2
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

        self.surf = pg.Surface((80, 100))
        self.surf.fill(PLAYER_COL)
        self.rect = self.surf.get_rect(center = self.pos)

    def update(self):
        #self.spring_force = pg.Vector2(0, 0)
        self.frame_skip = False
        self.starting_hand_pos = self.hand_pos.copy()

        # Hand movement
        if self.app.mouse[0]:
            self.hand_pos = self.pos.copy()
            self.hand_state = 'thrown'

        if self.app.mouse_pressed[0]:
            self.hand_target = (self.app.mouse_pos - self.app.screen_off + self.app.world_position) 
        else:

            self.hand_target = self.pos.copy()
            
               
        if self.hand_state == 'thrown' or self.hand_state == 'attached':
            
            self.displacement_to_target = (self.hand_target - self.hand_pos)
            self.distance_to_target = self.displacement_to_target.length()
            
            if self.distance_to_target != 0:
                if self.distance_to_target >= HAND_DISTANCE_DROPOFF:
                    self.distance_to_target = 1
                else:
                    self.distance_to_target /= HAND_DISTANCE_DROPOFF
                
                self.hand_vel = self.displacement_to_target.normalize()
                self.hand_vel *= HAND_SPEED * (math.cos((1 - self.distance_to_target) * 1.3)) # add delta time
            self.hand_pos += self.hand_vel   
            if self.hand_pos.distance_to(self.hand_target) <= HAND_SPEED * (math.cos((1 - self.distance_to_target) * 1.3)):
                self.hand_pos = self.hand_target.copy()
                self.hand_vel = pg.Vector2(0, 0)
                
                if self.is_hand_attached() and self.attached == False and self.hand_pos != self.pos: # put these other conditions in the function
                    if self.hand_state != 'attached':
                        self.frame_skip = True
                    self.hand_state = 'attached'
                    
                    #self.arm_length = (self.hand_pos - self.pos).length()

                if self.hand_pos == self.pos:
                    self.hand_state = 'ready'

        #print(self.hand_state, self.attached) 
        # Player movement
        self.gravity = pg.Vector2(0, GRAVITY)
        self.gravity = pg.Vector2(0, 0)
        # Gravity
        if self.hand_state == 'attached' and not self.frame_skip:
            #print('here', self.hand_pos)
            if self.app.mouse_pressed[0]:
                self.vel = pg.Vector2(0, 0)
                self.pos += (self.starting_hand_pos - self.hand_pos)
                self.saved_vel = (self.starting_hand_pos - self.hand_pos).copy()
                self.hand_pos = self.starting_hand_pos.copy()
            
            if not self.app.mouse_pressed[0]:
                self.hand_state = 'thrown'
                self.vel = self.saved_vel


        # here so rendering is fixed
         
        # Useful code here posiblely
            '''
            print('here', self.hand_pos)
            self.arm_diff = self.hand_pos - self.pos
            self.arm_extension = self.arm_diff.length() - self.arm_length
            self.spring_force_mag = ARM_SPRING_CONSTANT * self.arm_extension
            #self.spring_force_dir = math.atan2(self.arm_diff.y, self.arm_diff.x)
            
            self.spring_force = self.arm_diff.normalize() * self.spring_force_mag  
            #print(math.degrees(self.spring_force_dir))
            '''  
        

        self.vel += self.gravity * self.app.dt
        #self.total_force = self.gravity + self.spring_force
        #self.vel += self.total_force * self.app.dt/ MASS
        # Add velocity
        self.pos += self.vel
        self.hand_pos += self.vel
        self.rect.center = self.pos

    def is_hand_attached(self):

        return True

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



# after code refactor - 
# determine a target for the player position
# use the same code for the hand movement to determine a counter force to get to the target
# then add on the gravity force and air resistance
# which means the other vels and stuff need to be turned into a force
# that should give a good movement system






