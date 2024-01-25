import pygame
import os

WIN_WIDTH = 500
WIN_HEIGHT = 800
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("images/bird1.png")),pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))),pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5


    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.frame_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        
        self.bird_mask = pygame.mask.from_surface(self.img)        

    def jump(self):
        self.vel = -11
        self.frame_count = 0
        self.height = self.y

    def move(self):
        self.frame_count += 1
        displacement = self.vel*self.frame_count + 1.5*(self.frame_count**2) #REVIEW!!

        if displacement >= 15:
             displacement = 15

        if displacement < 0:
            displacement -= 2

        self.y  = self.y + displacement

        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        
        if self.y < 0:
            self.y = 0
            
        if self.y > WIN_HEIGHT - 50:
            self.y = WIN_HEIGHT - 50
            self.tilt = 0
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self,win):
        self.img_count += 1

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rot_img = pygame.transform.rotate(self.img, self.tilt)
        rect = rot_img.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        self.bird_mask = pygame.mask.from_surface(rot_img)
        win.blit(rot_img, rect.topleft)

