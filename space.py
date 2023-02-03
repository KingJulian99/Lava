from PIL import Image
import numpy as np

class Space:

    def __init__(self, resolution_x, resolution_y, particles):
        self.resolution_x = resolution_x
        self.resolution_y = resolution_y
        self.particles = particles
        self.space = []
        self.temperatures = []

        for y in range(self.resolution_y):
            row = []
            for x in range(self.resolution_x):
                row.append(0.0)
            self.space.append(row)
            self.temperatures.append(row)


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

            for y in range(-5, 5):

                for x in range(-5 + abs(y), 5 - abs(y)):

                    if( 0 <= ( int (self.resolution_y - 1) - int (y_position) - y ) <= (len(self.space) - 1) and 0 <= (int (x_position) - x) <= (len(self.space[0]) - 1)):

                        self.space[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        self.temperatures[int (self.resolution_y - 1) - int (y_position) - y][int (x_position) - x] = (particle.temperature / 3.0)


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
                    pixel_row.append((min(100 * self.temperatures[y][x], 255), 100, 100))
                else:
                    pixel_row.append((0, 0, 0))

            pixels.append(pixel_row)

        return pixels



    