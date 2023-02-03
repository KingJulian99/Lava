from particle import Particle
from space import Space
import cv2
import os
import random

particles = []
for p in range(200):
    particles.append(Particle(random.random(), random.random(), (0.0, 0.0), 0.0, -0.011))

space = Space(1000,1000, particles)

TOTAL_FRAMES = 2000

for i in range(TOTAL_FRAMES):

    for particle in particles:
        particle.updateVelocity(particles)
        particle.updateTemperature()
        particle.updatePosition()

    space.updateGrid()

    space.saveGridImage(f'images/{i}.png')

image_folder = 'images'
video_name = 'video.avi'

images = [f"{i}.png" for i in range(TOTAL_FRAMES)]

print(images)

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 30, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()