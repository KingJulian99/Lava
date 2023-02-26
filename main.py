from particle import Particle
from space import Space
import cv2
import os
import random
import time

particles = []
for p in range(30):
    particles.append(Particle(random.random(), random.random(), (0.0, 0.0), 0.0, -0.011))

space = Space(400,400, particles)

TOTAL_FRAMES = 3000

times = []

for i in range(TOTAL_FRAMES):

    start_time = time.perf_counter()

    for particle in particles:
        particle.updateVelocity(particles)
        particle.updateTemperature()

    for particle in particles:
        particle.updatePosition()

    space.updateGridCircle()

    space.saveGridImage(f'images/{i}.png')

    space.clearTemps()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    #print("Elapsed time for one frame: ", elapsed_time, " seconds")

    times.append(elapsed_time)


print("average time for a frame: " + str(sum(times) / len(times)))

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