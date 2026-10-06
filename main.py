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
FINISH_MASK = pygame.mask.from_surface(FINISH)
RED_CAR = scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","red-car.png")),0.55)
GREEN_CAR= scale_image(pygame.image.load(os.path.join(BASE_DIR,"imgs","green-car.png")),0.55)
FINISH_POSITION = (110,240)
PATH = [(134, 150), (80, 65), (49, 355), (108, 431), (205, 524), (293, 564), (318, 446), (375, 371), (464, 412), (479, 547), (559, 570), (574, 469), (566, 293), (566, 293), (431, 282), (331, 270), (332, 200), (469, 190), (574, 177), (570, 66), (458, 50), (256, 56), (218, 99), (217, 192), (204, 308), (136, 258)]
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

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (143,200)
    def reduce_speed(self):
        self.vel = max((self.vel - self.accelaration)/2,0)
        self.move()
    def bounce(self):
        self.vel = -self.vel
        self.move()


class ComputerCar(AbstractCar):
        IMG = GREEN_CAR
        START_POS = (117,200)

        def __init__(self, max_vel, rotation_vel,path=[]):
            super().__init__(max_vel, rotation_vel)
            self.path = path
            self.current_point = 0
            self.vel = max_vel

        def draw_points(self,win):
            for point in self.path:
                pygame.draw.circle(win,(0,255,0),point,5)

        def draw(self,win):
            super().draw(win)
            self.draw_points(win)

        def calculate_angle(self):
            target_x, target_y = self.path[self.current_point]
            x_diff = target_x - self.x
            y_diff = target_y - self.y

            if y_diff == 0:
                desired_radian_angle = math.pi / 2
            else:
                desired_radian_angle = math.atan(x_diff/y_diff)

            if target_y > self.y:
                desired_radian_angle += math.pi 

            difference_in_angle = self.angle - math.degrees(desired_radian_angle)
            if difference_in_angle >= 180:
                difference_in_angle -= 360

            if difference_in_angle>0:
                self.angle -= min(self.rotation_vel , abs(difference_in_angle))
            else:
                self.angle += min(self.rotation_vel , abs(difference_in_angle))

        def update_path_point(self):
            target = self.path[self.current_point]
            rect = pygame.Rect(self.x,self.y,self.img.get_width(),self.img.get_height())
            if rect.collidepoint(*target):
                self.current_point += 1


        def move(self):
            if self.current_point >= len(self.path):
                return 
            self.calculate_angle()
            self.update_path_point()
            super().move()



def draw(win,images,player_car,computer_car):
    for img,pos in images:
        win.blit(img,pos)
    player_car.draw(win)
    computer_car.draw(win)
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

def handle_collision(player_car,computer_car):
    if player_car.collide(TRACK_BORDER_MASK)!=None:
        player_car.bounce()
    
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK,*FINISH_POSITION) 
    if computer_finish_poi_collide != None:
        player_car.reset()
        computer_car.reset()
    
    player_finish_poi_collide = player_car.collide(FINISH_MASK,*FINISH_POSITION) 
    if player_finish_poi_collide!= None:
        if player_finish_poi_collide[1] == 0:
            player_car.bounce()
        else:
            player_car.reset()
            computer_car.reset()

images = [
    ( GRASS , (0,0) ),
    ( TRACK , (0,0) ),
    ( FINISH , FINISH_POSITION ),
    ( TRACK_BORDER , (0,0) )
    ]

player_car = PlayerCar(4,4)
computer_car = ComputerCar(2,2,PATH)
clock = pygame.time.Clock()
while run:
    clock.tick(FPS)

    draw(WIN,images,player_car,computer_car)
    computer_car.draw(WIN)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_player(player_car)
    computer_car.move()
    handle_collision(player_car,computer_car)

    

pygame.quit()

