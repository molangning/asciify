#!/usr/bin/python3
import os,time

from PIL import ImageOps, Image, ImageStat, ImageSequence
import json, base64
frames=[]

im = Image.open("sample_images/7fqm56-1959674893.gif")

for frame in ImageSequence.Iterator(im):

    temp = [frame.info['duration']/1000]

    width, height = frame.size
    aspect_ratio = height/width
    new_width = 180 # Original is 120
    new_height = aspect_ratio * new_width * 0.55
    frame = frame.resize((new_width, int(new_height))).convert('RGB')

    img_grayscale = frame.convert('L')

    if ImageStat.Stat(img_grayscale).mean[0] > 128:
        img_grayscale = ImageOps.invert(frame).convert('L')


    chars = ["@", "."]
    
    pixels = img_grayscale.getdata()

    new_pixels = []
    for pixel in pixels:
        new_pixels.append(chars[pixel//128])

    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)+'\n'
    
    temp.append(ascii_image)
    frames.append(temp)


import lzma

open('run-gif.py','w').write("#!/bin/python3\n\n"+rf"""exec('import json,base64,time,lzma\nframes=json.loads(lzma.decompress(base64.b64decode("{base64.b64encode(lzma.compress(json.dumps(frames).encode('utf-8'))).decode('utf-8')}")))\nwhile True:\n for i in frames:\n  print("\x1B[2J\x1B[H")\n  print(i[1])\n  time.sleep(i[0])')""")
