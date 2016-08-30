import pygame
import time

pygame.init()
pygame.joystick.init()

pygame.event.set_blocked([pygame.VIDEORESIZE,pygame.VIDEOEXPOSE])

class Joystick:
    def __init__(self,index=0):
        self.pjoy = pygame.joystick.Joystick(index)
        self.pjoy.init()

    def process(self):
        pygame.event.pump()

    def get_hat(self,index,up):
        return self.pjoy.get_hat(0)[index] == [-1,1][up]

    def get_axis(self,index,up):
        return self.pjoy.get_axis(index)*[-1,1][up] > 0.3

    def get_key(self,index):
        return self.pjoy.get_button(index)

    def get_free(self,idstring):
        if idstring[0] == "b":
            return self.get_key(int(idstring[1:])-1)
        elif idstring[0] == "l":
            return self.get_axis(0,idstring[1] in "+dl") and self.get_axis(1,idstring[1] in "+dl")
        elif idstring[0] == "r":
            return self.get_axis(2, idstring[1] in "+dl") and self.get_axis(3, idstring[1] in "+dl")
        elif idstring[0] == "h":
            return self.get_hat(0, idstring[1] in "+dl") and self.get_axis(1, idstring[1] in "+dl")

    def get_first(self,strl):
        l = strl.split(";")
        for i,v in enumerate(l):
            if self.get_free(v):
                yield i