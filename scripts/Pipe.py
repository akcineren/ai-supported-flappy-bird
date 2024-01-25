import pygame
import random
import os

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "pipe.png")))


class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self,x):
        self.x = x
        self.height = 0
        self.gap = 100
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        
        
        # This three lines can be used to adjust the width of the pipes. Default value is 2.
        # divider = 2
        #self.PIPE_TOP = pygame.transform.scale(self.PIPE_TOP, (self.PIPE_TOP.get_width()/divider,self.PIPE_TOP.get_height()))
        #self.PIPE_BOTTOM = pygame.transform.scale(self.PIPE_BOTTOM, (self.PIPE_BOTTOM.get_width()/divider,self.PIPE_BOTTOM.get_height()))

        self.QUEUE_CHECK = False
        self.passed = False
        self.set_height()
        
        self.pipeTop_mask = pygame.mask.from_surface(self.PIPE_TOP)
        self.pipeTop_mask_img = self.pipeTop_mask.to_surface()
        
        self.pipeBottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        self.pipeBottom_mask_img = self.pipeBottom_mask.to_surface()
    
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL
    
    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    