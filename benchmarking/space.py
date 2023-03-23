from math import sqrt
import math
from PIL import Image
import numpy as np
import time
import external_methods

class Space:

    def __init__(self, resolution_x, resolution_y, particles):
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.particles = particles
        self.space = []
        self.temperatures = []
        self.PARTICLE_RADIUS = 18
        self.RED_FACTOR = 0.5
        self.GREEN_FACTOR = 0.0
        self.BLUE_FACTOR = 0.5

        for y in range(self.resolution_y):
            row = []
            for x in range(self.resolution_x):
                row.append(0.0)
            self.space.append(row)
            self.temperatures.append(row)

    
    def getDistance(self, x1, y1, x2, y2):
        return math.dist((x1, y1), (x2, y2))


    def getNormalizedDistance(self, x1, y1, x2, y2, radius):
        return self.getDistance(x1, y1, x2, y2) / radius
    


    def printGrid(self):
        for y in range(self.resolution_y):
            print(self.space[y])


    def updateGrid(self):
        self.clearGrid()

        step_x = 1.0/self.resolution_x
        step_y = 1.0/self.resolution_y
        
        for particle in self.particles:
            # Find the visual grid position of the particle and set to 1.0 
            y_position = particle.y_coord // step_y
            x_position = particle.x_coord // step_x

            for y in range(-self.PARTICLE_RADIUS, self.PARTICLE_RADIUS):

                for x in range(-self.PARTICLE_RADIUS + abs(y), self.PARTICLE_RADIUS - abs(y)):

                    if( 0 <= ( int (self.resolution_y - 1) - int (y_position) - y ) <= (len(self.space) - 1) and 0 <= (int (x_position) - x) <= (len(self.space[0]) - 1)):

                        self.space[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = (particle.temperature / 3.0)


    def externalUpdateGridCircle(self):
        space_array = np.array(self.space, dtype=np.float32)
        temp_array = np.array(self.temperatures, dtype=np.float32)
        external_methods.updateGridCircle(self, self.resolution_y, self.resolution_x, self.PARTICLE_RADIUS, space_array, temp_array)

        self.space = space_array.tolist()
        self.temperatures = temp_array.tolist()

    
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

                    if(external_methods.liesInBounds(self.resolution_y, self.resolution_x, y_position, x_position, y, x, len(self.space), len(self.space[0]))): 

                        self.space[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        #self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = (self.getNormalizedDistance(x, y, 0, 0, self.PARTICLE_RADIUS) * 2.0)
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] += (2.0 - min(1.0, (self.getNormalizedDistance(x, y, 0, 0, self.PARTICLE_RADIUS))) * 2.0)


    # C
    def liesInBounds(self, y_center_position, x_center_position, y, x):
        if( 0 <= ( int (self.resolution_y - 1) - int (y_center_position) - y ) <= (len(self.space) - 1) and 0 <= (int (x_center_position) - x) <= (len(self.space[0]) - 1)):
            return True
        else:
            return False
        
    # C - changes python data though? 
    def updateGridCircle2(self):
        self.clearGrid()

        step_x = 1.0/self.resolution_x
        step_y = 1.0/self.resolution_y
        
        for particle in self.particles:
            y_position = particle.y_coord // step_y
            x_position = particle.x_coord // step_x

            for y in range(0, self.PARTICLE_RADIUS):

                if(y == 0):
                    width = self.PARTICLE_RADIUS
                else:
                    width = sqrt(self.PARTICLE_RADIUS**2 - y**2)

                
                for x in range(- int (width), int (width)):                    
                    if(self.liesInBounds(y_position, x_position, y, x)): 
                        self.space[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] += (2.0 - min(1.0, (self.getNormalizedDistance(x, y, 0, 0, self.PARTICLE_RADIUS))) * 2.0)

                    if(self.liesInBounds(y_position, x_position, -y, x)): 
                        self.space[int (self.resolution_y - 1) - int (y_position) - (-y)][int (x_position) - x] = 1.0
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - (-y)][int (x_position) - x] += (2.0 - min(1.0, (self.getNormalizedDistance(x, -y, 0, 0, self.PARTICLE_RADIUS))) * 2.0)



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

    
    
    def generateGridArray(self):
        pixels = self.gridToPixels()

        array = np.array(pixels, dtype=np.uint8)

        new_image = Image.fromarray(array)
        new_image = new_image.resize((60, 60), resample=Image.BOX)
        new_image = new_image.resize((40, 40), resample=Image.BOX)
        new_image = new_image.resize((10, 10), resample=Image.BOX)

        return np.asarray(new_image)


    def saveGridImage(self, array, output_filename):

        new_image = Image.fromarray(array)
        
        new_image = new_image.resize((60, 60), resample=Image.BOX)
        new_image = new_image.resize((40, 40), resample=Image.BOX)
        new_image = new_image.resize((10, 10), resample=Image.BOX)

        new_image.save(output_filename)

        return new_image

    
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
                    height = max( 0.0, min(self.temperatures[y][x] * 25, 255) )
                    pixel_row.append( ( self.RED_FACTOR * height, self.GREEN_FACTOR * height, self.BLUE_FACTOR * height ) )
                else:
                    pixel_row.append((0, 0, 0))

            pixels.append(pixel_row)

        return pixels


    def generateInterpolatedImages(self, old_array, new_array, FRAME_COUNT, frame_number):
        old_array = old_array.tolist()
        new_array = new_array.tolist()
        
        for i in range(FRAME_COUNT):
            pixels = []

            for y in range(self.resolution_y):
                pixel_row = []
                for x in range(self.resolution_x):

                    tupleDifference = self.getTupleDifference(old_array[y][x], new_array[y][x])

                    pixel_row.append( (old_array[y][x][0] + (tupleDifference[0]/FRAME_COUNT)*(i + 1), old_array[y][x][1] + (tupleDifference[1]/FRAME_COUNT)*(i + 1), old_array[y][x][2] + (tupleDifference[2]/FRAME_COUNT)*(i + 1)) )

                pixels.append(pixel_row)

            array = np.array(pixels, dtype=np.uint8)

            new_interpolated_image = Image.fromarray(array)

            new_interpolated_image = new_interpolated_image.resize((60, 60), resample=Image.BOX)
            new_interpolated_image = new_interpolated_image.resize((40, 40), resample=Image.BOX)
            new_interpolated_image = new_interpolated_image.resize((10, 10), resample=Image.BOX)

            new_interpolated_image.save(f'images/{frame_number}.png')

            frame_number += 1

        return frame_number


    def getTupleDifference(self, tupleOne, tupleTwo):
        return ((tupleTwo[0] - tupleOne[0]), (tupleTwo[1] - tupleOne[1]), (tupleTwo[2] - tupleOne[2]))
