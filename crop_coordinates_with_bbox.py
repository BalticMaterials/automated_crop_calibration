from PIL import Image, ImageFilter, ImageChops, ImageDraw
filename = "images/1701101199586.tiff"# "images/1701101741803.tiff"
threshold_blue = 100
threshold_red = 150

with Image.open(filename) as img:
    img.load()
    red, green, blue = img.split()
   
    img_blue_threshold = blue.point(lambda x: 255 if x > threshold_blue else 0)
    img_blue_threshold = img_blue_threshold.convert("1")
    
    img_red_threshold = red.point(lambda x: 255 if x > threshold_red else 0)
    img_red_threshold = img_red_threshold.convert("1")
    

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
    
    img.crop(img_threshold.getbbox()).show()
    f = open("bbox_coordinates.txt", "w")
    f.write(str(img_threshold.getbbox()))
    f.close()
