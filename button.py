import pygame
from settings import *

class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        # check if mouse is on button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        return action