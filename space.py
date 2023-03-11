from math import sqrt
from PIL import Image
import numpy as np
import time

class Space:

    def __init__(self, resolution_x, resolution_y, particles):
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.particles = particles
        self.space = []
        self.temperatures = []
        self.PARTICLE_RADIUS = 66

        for y in range(self.resolution_y):
            row = []
            for x in range(self.resolution_x):
                row.append(0.0)
            self.space.append(row)
            self.temperatures.append(row)

    
    def getDistance(self, x1, y1, x2, y2):
        return sqrt((x1-x2)**2 + (y1-y2)**2)


    def getNormalizedDistance(self, x1, y1, x2, y2, radius):
        return self.getDistance(x1, y1, x2, y2) / radius
    


    def printGrid(self):
        for y in range(self.resolution_y):
            print(self.space[y])


    def updateGrid(self):
        # Set all to 0.0
        self.clearGrid()

        step_x = 1.0/self.resolution_x
        step_y = 1.0/self.resolution_y
        
        for particle in self.particles:
            # Find the visual grid position of the particle and set to 1.0 
            y_position = particle.y_coord // step_y
            x_position = particle.x_coord // step_x

            #self.space[int (self.resolution_y - 1) - int (y_position)][int (x_position)] = 1.0

            for y in range(-self.PARTICLE_RADIUS, self.PARTICLE_RADIUS):

                for x in range(-self.PARTICLE_RADIUS + abs(y), self.PARTICLE_RADIUS - abs(y)):

                    if( 0 <= ( int (self.resolution_y - 1) - int (y_position) - y ) <= (len(self.space) - 1) and 0 <= (int (x_position) - x) <= (len(self.space[0]) - 1)):

                        self.space[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = (particle.temperature / 3.0)

    
    def updateGridCircle(self):
        self.clearGrid()

        step_x = 1.0/self.resolution_x
        step_y = 1.0/self.resolution_y
        
        for particle in self.particles:
            y_position = particle.y_coord // step_y
            x_position = particle.x_coord // step_x

            for y in range(-self.PARTICLE_RADIUS, self.PARTICLE_RADIUS):
                height = abs(y)

                if(height == 0):
                    width = self.PARTICLE_RADIUS
                else:
                    width = sqrt(self.PARTICLE_RADIUS**2 - height**2)

                for x in range(- int (width), int (width)):

                    if( 0 <= ( int (self.resolution_y - 1) - int (y_position) - y ) <= (len(self.space) - 1) and 0 <= (int (x_position) - x) <= (len(self.space[0]) - 1)):

                        self.space[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        #self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = (self.getNormalizedDistance(x, y, 0, 0, self.PARTICLE_RADIUS) * 2.0)
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] += (2.0 - min(1.0, (self.getNormalizedDistance(x, y, 0, 0, self.PARTICLE_RADIUS))) * 2.0)



    def clearTemps(self):
        self.temperatures = []

        for y in range(self.resolution_y):
            row = []
            for x in range(self.resolution_x):
                row.append(0.0)
            self.temperatures.append(row)



    def clearGrid(self):
        self.space = []

        for y in range(self.resolution_y):
            row = []
            for x in range(self.resolution_x):
                row.append(0.0)
            self.space.append(row)


    def saveGridImage(self, output_filename):
        pixels = self.gridToPixels()

        array = np.array(pixels, dtype=np.uint8)

        new_image = Image.fromarray(array)
        #new_image = new_image.resize((self.resolution_x//2, self.resolution_y//2), resample=Image.BOX)
        #new_image = new_image.resize((self.resolution_x//2, self.resolution_y//2), resample=Image.BOX)
        #new_image = new_image.resize((self.resolution_x//2, self.resolution_y//2), resample=Image.BOX)
        #new_image = new_image.resize((10, 10), resample=Image.BOX)

        new_image.save(output_filename)

    
    def generateGridImage(self):
        pixels = self.gridToPixels()

        array = np.array(pixels, dtype=np.uint8)

        new_image = Image.fromarray(array)

        return new_image


    def gridToPixels(self):
        pixels = []

        for y in range(self.resolution_y):
            pixel_row = []
            for x in range(self.resolution_x):

                if(self.space[y][x] == 1.0):
                    height = max( 0.0, min(self.temperatures[y][x] * 35, 254) )
                    pixel_row.append( ( 0.0, height // 4, height ) )
                else:
                    pixel_row.append((0, 0, 0))

            pixels.append(pixel_row)

        return pixels

    