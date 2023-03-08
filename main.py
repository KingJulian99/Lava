from particle import Particle
from space import Space
import cv2
import os
import random
import time

particles = []
for p in range(30):
    particles.append(Particle(random.random(), random.random(), (0.0, 0.0), 0.0, -0.011))

space = Space(100,100, particles)

TOTAL_FRAMES = 300
INTERPOLATION_FRAME_COUNT = 4

times = []

frame_number = 0
prev_image = None
has_been_prev_image = False
for i in range(TOTAL_FRAMES):

    start_time = time.perf_counter()

    for particle in particles:
        particle.updateVelocity(particles)
        particle.updateTemperature()

    for particle in particles:
        particle.updatePosition()

    space.updateGridCircle()

    array = space.generateGridArray()

    if (has_been_prev_image and INTERPOLATION_FRAME_COUNT > 0):
        frame_number = space.generateInterpolatedImages(prev_image, array, INTERPOLATION_FRAME_COUNT, frame_number)

    space.saveGridImage(array, f'images/{frame_number}.png')

    prev_image = array
    has_been_prev_image = True

    space.clearTemps()

    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    #print("Elapsed time for one frame: ", elapsed_time, " seconds")

    times.append(elapsed_time)

    color_change_increment = 0.075

    # if(frame_number >= 800):
    #     space.RED_FACTOR += color_change_increment
    #     space.BLUE_FACTOR -= color_change_increment

    # if (space.RED_FACTOR > 1.0):
    #     space.RED_FACTOR = 1.0

    # if (space.BLUE_FACTOR < 0.0):
    #     space.BLUE_FACTOR = 0.0

    # if (space.GREEN_FACTOR > 1.0):
    #     space.GREEN_FACTOR = 0.0

    frame_number += 1


print("average time for a frame: " + str(sum(times) / len(times)))

image_folder = 'images'
video_name = 'video.avi'

images = [f"{i}.png" for i in range(TOTAL_FRAMES)]

print(images)

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 90, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()