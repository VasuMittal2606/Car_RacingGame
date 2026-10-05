import pygame
import time
import math
from util import *
import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#SETTING FIXED VARIABLES IN ALL-CAPS FOR THE ELEMENTS
GRASS = scale_image(pygame.image.load( os.path.join(BASE_DIR,"imgs","grass.jpg") ),2.5)
TRACK = scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","track.png")),0.9)
TRACK_BORDER = scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","track-border.png")),0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
FINISH = scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","finish.png")),0.75)
RED_CAR = scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","red-car.png")),0.55)
GREEN_CAR= scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","green-car.png")),0.55)

#SETTING UP THE DISPLAY WINDOW
WIDTH,HEIGHT = TRACK.get_width(), TRACK.get_height()
FPS = 60
run = True

WIN = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Racing game")


class AbstractCar:
    IMG = RED_CAR
    def __init__(self,max_vel,rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x,self.y = self.START_POS
        self.accelaration = 0.1

    def rotate(self,left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw(self,win):
        blit_rotate_center(win,self.img,(self.x,self.y),self.angle)

    def move_foward(self):
        self.vel = min(self.vel + self.accelaration, self.max_vel)
        self.move()
    
    def move_backward(self):
        self.vel = min(self.vel - self.accelaration, self.max_vel/2)
        self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians)*self.vel
        self.y -= vertical
        self.x -= horizontal

    def collide(self,mask,x=0,y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x ),int(self.y - y))
        poi = mask.overlap(car_mask,offset)
        return poi

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (130,200)
    def reduce_speed(self):
        self.vel = max((self.vel - self.accelaration)/2,0)
        self.move()


def draw(win,images,player_car):
    for img,pos in images:
        win.blit(img,pos)
    player_car.draw(win)
    pygame.display.update()

def move_player(player_car):
    keys = pygame.key.get_pressed()
    moved =False
    if keys[pygame.K_a]:
        player_car.rotate(left = True)
    if keys[pygame.K_d]:
        player_car.rotate(right = True)
    if keys[pygame.K_w]:
        moved = True
        player_car.move_foward()
    if keys[pygame.K_s]:
        moved = True
        player_car.move_backward()
    if not moved:
        player_car.reduce_speed()

images = [
    ( GRASS , (0,0) ),
    ( TRACK , (0,0) ),
    ( TRACK_BORDER , (0,0) ),
    ( FINISH , (0,0) ),
    ( RED_CAR , (0,0) ),
    ( GREEN_CAR , (0,0) )
    ]

player_car = PlayerCar(5,5)
clock = pygame.time.Clock()
while run:
    clock.tick(FPS)

    draw(WIN,images,player_car)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    if player_car.collide(TRACK_BORDER_MASK)!=None:
        print("COllide")

pygame.quit()

