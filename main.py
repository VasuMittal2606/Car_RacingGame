import pygame
import time
import math
from util import scale_image

#SETTING FIXED VARIABLES IN ALL-CAPS FOR THE ELEMENTS
GRASS = scale_image(pygame.image.load("Car_RacingGame/imgs/grass.jpg"),2.5)
TRACK = scale_image(pygame.image.load("Car_RacingGame/imgs/track.png"),0.9)
TRACK_BORDER = scale_image(pygame.image.load("Car_RacingGame/imgs/track-border.png"),0.9)
FINISH = scale_image(pygame.image.load("Car_RacingGame/imgs/finish.png"),0.75)
RED_CAR = scale_image(pygame.image.load("Car_RacingGame/imgs/red-car.png"),0.55)
GREEN_CAR= scale_image(pygame.image.load("Car_RacingGame/imgs/green-car.png"),0.55)

#SETTING UP THE DISPLAY WINDOW
WIDTH,HEIGHT = TRACK.get_width(), TRACK.get_height()
FPS = 60
run = True

WIN = pygame.display.set_mode((WIDTH,HEIGHT),pygame.RESIZABLE)
pygame.display.set_caption("Racing game")

def draw(win,images):
    for img,pos in images:
        win.blit(img,pos)

images = [
    ( GRASS , (0,0) ),
    ( TRACK , (0,0) ),
    ( TRACK_BORDER , (0,0) ),
    ( FINISH , (0,0) ),
    ( RED_CAR , (0,0) ),
    ( GREEN_CAR , (0,0) )
    ]

clock = pygame.time.Clock()
while run:
    clock.tick(FPS)

    draw(WIN,images)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break



pygame.quit()