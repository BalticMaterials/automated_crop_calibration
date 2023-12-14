""" Programm for identifying the blue conveyor belt on images taken by the OAK-1 MAX.
A text file with the crop coordinates on the original image is produced in the end.
Program works only good if the conveyor belt runs vertically or horizontally through the image.
For other postures refer to "conveyor_belt_identification.py"!
"""

__author__ = "Sven Nivera"
__contact__ = "sven.nivera@balticmaterials.de"
__date__ = "2023/12/14"
__deprecated__ = False
__license__ = "CC0 1.0 Universal"
__maintainer__ = "Sven Nivera"
__status__ = "Deployable"
__version__ = "1.0.1"
__annotations__ = "Software can be used as basis for further specialized calibrations! Only manual access now"

from PIL import Image, ImageFilter, ImageChops
import time 
filename = "images/1701101199586.tiff"
session_name = "bbox_coordinates_" + str(time.time())
threshold_blue = 100
threshold_red = 150

with Image.open(filename) as img:
    img.load()
    red, green, blue = img.split()


    # Thresholding blue and red channels to isolate the blue conveyor belt from the background and conveyor chasis
    img_blue_threshold = blue.point(lambda x: 255 if x > threshold_blue else 0)
    img_blue_threshold = img_blue_threshold.convert("1")
    
    img_red_threshold = red.point(lambda x: 255 if x > threshold_red else 0)
    img_red_threshold = img_red_threshold.convert("1")
    

    # Enhancing the channels
    def erode(cycles, image):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MinFilter(3))
        return image

    def dilate(cycles, image):
        for _ in range(cycles):
            image = image.filter(ImageFilter.MaxFilter(3))
        return image
        
    img_blue_threshold = erode(10, img_blue_threshold)
    img_red_threshold = erode(10, img_red_threshold)
    
    # Creating a new image utilizing the blue and red channel to better isolate the blue conveyor belt from the conveyors metal frame
    img_threshold = ImageChops.logical_and(img_blue_threshold, ImageChops.invert(img_red_threshold))
    

    # Cropping image and saving coordinates of crop area
    img.crop(img_threshold.getbbox()).show()
    f = open(session_name + ".txt", "w")
    f.write(str(img_threshold.getbbox()))
    f.close()
