from pixel import Pixel

class Frame:
    def __init__(self):
        self.matrix = []
        for row in range(10):
            row = []
            for col in range(10):
                row.append(Pixel())
            self.matrix.append(row)

    def setPixel(self, row, col, color):
        #update('Setting pixel color inside frame..')
        self.matrix[row][col].setColor(color)
        #update('New pixel value: ' + str(self.matrix[row][col].getColor()))

    def getPixel(self, row, col):
        return self.matrix[row][col]
    
    def update(self, strip):
        #update('frame is updating the strip')
        for row in range(10):
            for col in range(10):
                strip.setPixelColor((row*10) + col, self.matrix[row][col].getColor())
        return strip