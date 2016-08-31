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
        pygame.event.wait()

    def get_hat(self,index,up):
        return self.pjoy.get_hat(0)[index] == [-1,1][up]

    def get_axis(self,index,up):
        return self.pjoy.get_axis(index)*[-1,1][up] > 0.7

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

    def get_axis_pole(self,axis):
        if axis == "l":
            x = self.get_axis(0,True) - self.get_axis(0,False)
            y = self.get_axis( 1, True) - self.get_axis( 1, False)
        if axis == "r":
            x = self.get_axis(2, True) - self.get_axis(2, False)
            y = self.get_axis(3, True) - self.get_axis(3, False)
        if axis == "h":
            x = self.get_hat(0, True) - self.get_hat(0, False)
            y = self.get_hat(1, True) - self.get_hat(1, False)
        return ((0,0),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,1)).index((x,y)) - 1

