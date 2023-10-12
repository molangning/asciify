#!/usr/bin/python3

# this code takes a image and generates a ascii representation of it
# in black and white with no in between colors
# if there is more lighter colors than darker colors, the code inverts the colors

# From https://www.askpython.com/python/examples/turn-images-to-ascii-art-using-python
# made the code more readable


import PIL.Image
import PIL.ImageOps
import PIL.ImageStat
import sys

if len(sys.argv)>1:
    imgs = sys.argv[1:]
else:   
    imgs = ["sample_images/boykisser.jpg"]

for img_name in imgs:
    img=PIL.Image.open(img_name)


    # try:
    #   img = PIL.Image.open(path)
    #   img_flag = True
    # except:
    #   print(path, "Unable to find image ");
    
    width, height = img.size
    aspect_ratio = height/width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img_grayscale = img.convert('L')

    # Check if mean value is higher or lower than the middle brightness
    # then invert accordingly
    # This is to get the most space to cram our code into

    if PIL.ImageStat.Stat(img_grayscale).mean[0] > 128:
        img_grayscale = PIL.ImageOps.invert(img).convert('L')


    chars = ["#", "."]
    
    pixels = img_grayscale.getdata()

    # max light level is 256, pixel//128 should work
    # what happens here is that we are converting the image into a 
    # ascii representation of two states, light and dark
    # may break for non line art
    # TODO: fix for non line art if possible

    new_pixels = []
    for pixel in pixels:
        new_pixels.append(chars[pixel//128])

    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)+'\n'
    
    with open("%s.txt"%("".join(img_name.split('.')[:-1])), "w") as f:
        f.write(ascii_image)