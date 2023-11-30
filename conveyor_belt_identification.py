""" Programm for identifying the blue conveyor belt on images taken by the OAK-1 MAX.
"""

__author__ = "Sven Nivera"
__contact__ = "sven.nivera@balticmaterials.de"
__date__ = "2023/11/30"
__deprecated__ = False
__license__ = "CC0 1.0 Universal"
__maintainer__ = "Sven Nivera"
__status__ = "Development"
__version__ = "0.2.3"
__annotations__ = "This program is only neccessary when the conveyor belt is not horizontal or vertical in the image. For the normal case use 'crop_coordinates_with_bbox.py'"

from PIL import Image, ImageFilter, ImageChops, ImageDraw
import numpy as np
filename =  "images/1701101741803.tiff"

threshold_blue = 100
threshold_red = 150
seed = (1500, 3000)

with Image.open(filename) as img:
    img.load()
    red, green, blue = img.split()

    # Thresholding blue and red channels to isolate the blue conveyor belt from the background and conveyor chasis
    print("Thresholding blue channel...")
    img_blue_threshold = blue.point(lambda x: 255 if x > threshold_blue else 0)
    img_blue_threshold = img_blue_threshold.convert("1")
    
    print("Thresholding red channel...")
    img_red_threshold = red.point(lambda x: 255 if x > threshold_red else 0)
    img_red_threshold = img_red_threshold.convert("1")
    

    # Enhancing the channels
    def erode(cycles, image):
        for i in range(cycles):
            print(str(round(((i / cycles) * 100), 2)) + "%")
            image = image.filter(ImageFilter.MinFilter(3))
        return image

    def dilate(cycles, image):
        for i in range(cycles):
            print(str(round(((i / cycles) * 100), 2)) + "%")
            image = image.filter(ImageFilter.MaxFilter(3))
        return image

    print("Erosion of blue channel...")    
    img_blue_threshold = erode(10, img_blue_threshold)
    print("Erosion of red channel...")
    img_red_threshold = erode(10, img_red_threshold)
    
    # Creating a new image utilizing the blue and red channel to better isolate the blue conveyor belt from the conveyors metal frame
    print('Channel merging...')
    img_threshold = ImageChops.logical_and(img_blue_threshold, ImageChops.invert(img_red_threshold))

    print('Step 1: Eroding...')
    step_1 = erode(12, img_threshold)
    
    print('Step 2: Dilating...')
    step_2 = dilate(58, step_1)

    print('Step 3: Eroding...')
    mask = erode(45, step_2)

    print('Step 4: Filling fully sorrounded spaces...')
    ImageDraw.floodfill(mask, seed, True) # Seed must be choosen manually!
    # To-Do: Add argument List capabilities           


    print('Creating composite image...')
    blank = img.point(lambda _: 0)
    segmented = Image.composite(img, blank, mask)
    segmented.show()
    segmented.save("segmentation.tiff")