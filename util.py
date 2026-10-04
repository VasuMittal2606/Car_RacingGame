import pygame
scale = 700/900
def scale_image(img,factor):
    size = (round(img.get_width()*factor*scale) ,round(img.get_height() * factor*scale))
    return pygame.transform.scale(img,size)
