from rpi_ws281x import *

class Pixel:
    def __init__(self):
        self.color = Color(0,0,0)

    def setColor(self, new_color):
        self.color = new_color

    def getColor(self):
        return self.color
