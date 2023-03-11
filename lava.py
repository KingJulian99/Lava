import time
from rpi_ws281x import *
import argparse
from PIL import Image
import os
from frame import Frame
from pixel import Pixel

LED_COUNT      = 100      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# class Pixel:
#     def __init__(self):
#         self.color = Color(0,0,0)

#     def setColor(self, new_color):
#         self.color = new_color

#     def getColor(self):
#         return self.color

# class Frame:
#     def __init__(self):
#         self.matrix = []
#         for row in range(10):
#             row = []
#             for col in range(10):
#                 row.append(Pixel())
#             self.matrix.append(row)

#     def setPixel(self, row, col, color):
#         #update('Setting pixel color inside frame..')
#         self.matrix[row][col].setColor(color)
#         #update('New pixel value: ' + str(self.matrix[row][col].getColor()))

#     def getPixel(self, row, col):
#         return self.matrix[row][col]
    
#     def update(self, strip):
#         #update('frame is updating the strip')
#         for row in range(10):
#             for col in range(10):
#                 strip.setPixelColor((row*10) + col, self.matrix[row][col].getColor())
#         return strip

# Define functions which animate LEDs in various ways.

class LED_CONTROLLER:

    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
        self.args = self.parser.parse_args()

        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

        self.frame = Frame()
        

    def colorWipe(self, strip, color, wait_ms=50):
        """Wipe color across display a pixel at a time."""
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, color)
            strip.show()
            time.sleep(wait_ms/1000.0)

    
    def firstTest(self, frame, i):
        #update('frame value -> ' + str(frame))
        #update('calling firstTest which should update pixels in frame')
        for row in range(10):
            for col in range(10):
                frame.setPixel(row, col, Color(i, 0, 0))


    def showImage(self, frame, strip, image_path):
        #print('showimage called')

        img = Image.open(f'{image_path}')
        img = img.convert('RGB')

        for row in range(10):
            for col in range(10):
                # get the RGB values of the current pixel
                r, g, b = img.getpixel((col, row))
                frame.setPixel(row, col, Color(r, g, b))

        strip = frame.update(strip)
        strip.show()


    def showGif(self, frame, strip, foldername, interval):
        n_files = len([name for name in os.listdir(f'gifs/{foldername}') if os.path.isfile(f'gifs/{foldername}/{name}')])

        for i in range(n_files):
            showImage(frame, strip, f'gifs/{foldername}/{i}.png')
            time.sleep(interval)


    @profile
    def showGridFrame(self, tuple_grid, time_interval_physics, time_interval_interpolated):
        for row in range(10):
            for col in range(10):
                r, g, b = tuple_grid[row][col][0], tuple_grid[row][col][1], tuple_grid[row][col][2]
                self.frame.setPixel(row, col, Color(r, g, b))

        self.strip = self.frame.update(self.strip)
        self.strip.show()


    def mainLoop(self, frame, strip, i):
        # clear all pixels
        #update('mainloop: clearning pixels..\nframe value -> ' + str(frame))
        #colorWipe(strip, Color(0,0,0), 10)

        while True:
            showGif(frame, strip, 'fractal2', 0.1)
            #showImage(frame, strip, 'images/heart1.png')
        #firstTest(frame, i)


    def showLava(self, frame, strip, tuple_grid, time_interval_physics, time_interval_interpolated):
        showGridFrame(frame, strip, tuple_grid, time_interval_physics, time_interval_interpolated)

    
    def test(self,strip):
        for i in range(10):
            strip.setPixelColor(i, Color(0,0,0))
            strip.setPixelColor(1+i, Color(255,255,0))
            strip.show()
