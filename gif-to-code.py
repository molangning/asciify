#!/usr/bin/python3

import os,time

from PIL import ImageOps, Image, ImageStat, ImageSequence
import json, base64
frames=[]

im = Image.open("sample_media/chipi-chipi-chapa-chapa-boykisser.gif")

for frame in ImageSequence.Iterator(im):

    temp = [frame.info['duration']/1000]

    width, height = frame.size
    aspect_ratio = height/width
    new_width = 400 # Original is 400
    new_height = aspect_ratio * new_width * 0.55
    frame = frame.resize((new_width, int(new_height))).convert('RGB')

    img_grayscale = frame.convert('L')

    if ImageStat.Stat(img_grayscale).mean[0] > 128:
        img_grayscale = ImageOps.invert(frame).convert('L')


    chars = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]
    
    grayscale_pixels = img_grayscale.getdata()
    color_pixels = frame.getdata()

    pixel_data=[[grayscale_pixels[i], color_pixels[i]] for i in range(len(grayscale_pixels))]
    new_pixels = []

    for gray_pixel, color_pixel in pixel_data:
        pixel = chars[int(gray_pixel//25)]
        pixel = "\x1b[38;2;%i;%i;%im%s\x1b[0m"%(color_pixel[0],color_pixel[1],color_pixel[2], pixel)
        new_pixels.append(pixel)    

    new_pixels_count = len(new_pixels)
    ascii_image = ["".join(new_pixels[index:index + new_width]) for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)+'\n'

    temp.append(ascii_image)
    frames.append(temp)


import lzma

# open("temp/raw_frames.json","w").write(json.dumps(frames))

open('run-gif.py','w').write("#!/bin/python3\n\nimport json,time\n"+rf'''exec(r"""a=json.loads(r'{json.dumps(frames)}')"""+'\nwhile True:\n for i in a:\n  print("\x1B[2J\x1B[H"+i[1],flush=True)\n  time.sleep(i[0]) break')''')
