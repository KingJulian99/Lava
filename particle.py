from math import sqrt
import random

class Particle:

    def __init__(self, x_coord, y_coord, velocity, temperature, gravity):
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.velocity = velocity
        self.temperature = temperature
        self.gravity = gravity
        self.RANDOM_FACTOR = random.random() * 0.2
        self.TEMP_INCREMENT = 0.65

    def updatePosition(self):
        self.x_coord += self.velocity[0]
        self.y_coord += self.velocity[1]

        if(self.x_coord < 0):
            self.x_coord = 0
            self.velocity = (0.001, self.velocity[1])

        elif(self.x_coord > 1):
            self.x_coord = 1
            self.velocity = (-0.001, self.velocity[1])

        if(self.y_coord < 0):
            self.y_coord = 0
            self.velocity = (self.velocity[0], 0.0)

        elif(self.y_coord > 1):
            self.y_coord = 1
            self.velocity = (self.velocity[0], 0.0)


    def updateVelocity(self, allParticles):
        # Updates the velocity of this particle. Currently doesn't support local neighbours 
        self.velocity = self.addGravity(self.velocity)
        self.velocity = self.addRandomness(self.velocity)

        for particle in allParticles:
            if particle != self:
                if(self.getDistance(self, particle) < 0.08):
                    if(self.getDistance(self, particle) < 0.01):
                        self.velocity = self.addRepulsion(self.velocity, particle)
                    else:
                        self.velocity = self.addAttraction(self.velocity, particle)

    def updateTemperature(self):
        if(self.temperature < 0):
            self.temperature = 0.0

        # Remove temperature if far away from heat source
        if(self.temperature > 0 and self.y_coord >= 0.3):
            self.temperature -= self.TEMP_INCREMENT * 0.5

        # Add temperature if close enough to floor
        if(self.y_coord < 0.3 and self.temperature <= 2.8):
            self.temperature += ( (2.0 - self.y_coord - self.RANDOM_FACTOR) ** 2 ) * self.TEMP_INCREMENT/2

    def addGravity(self, tupleOne):
        gravityDifference = self.velocity[1] - self.gravity

        return self.addTuple(self.velocity, (0, (1 - self.temperature) * ( self.terminalVelocityModifier(gravityDifference) * self.gravity ) ))

    def addRandomness(self, tupleOne):
        return self.addTuple(self.velocity, ( (random.random() - 0.5) / 2000 , (random.random() - 0.5) / 3000 ) )

    def getDistance(self, particleOne, particleTwo):
        return sqrt((particleOne.x_coord - particleTwo.x_coord)**2 + (particleOne.y_coord - particleTwo.y_coord)**2)

    def addAttraction(self, tupleOne, otherParticle):
        return self.addTuple(self.velocity, ( 0.35 * ( abs(3.0 - self.temperature)/3 ) * ( ( 0.15 - self.getDistance(self, otherParticle) ) * (otherParticle.velocity[0] - self.velocity[0]) ), 0.35 * ( abs(3.0 - self.temperature)/3 ) * ( ( 0.15 - self.getDistance(self, otherParticle) ) * (otherParticle.velocity[1] - self.velocity[1])) ))

    def addRepulsion(self, tupleOne, otherParticle):
        return self.addTuple(self.velocity, ( 0.05 * (self.x_coord - otherParticle.x_coord) * (1.0 - self.getDistance(self, otherParticle)) , 0.05 * (self.y_coord - otherParticle.y_coord) * (1.0 - self.getDistance(self, otherParticle)) ))

    def terminalVelocityModifier(self, gravityDifference):
        return 0 if gravityDifference <= 0 else min(gravityDifference, 1.0)

    def addTuple(self, tupleOne, tupleTwo):
        return (tupleOne[0] + tupleTwo[0], tupleOne[1] + tupleTwo[1])
