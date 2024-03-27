#!/usr/bin/env python3

import struct
import argparse
from PIL import ImageOps, Image, ImageStat, ImageSequence

parser = argparse.ArgumentParser(description='Converts gif into runnder code')
parser.add_argument('--input', type=str, help='input gif', default="sample_media/chipi-chipi-chapa-chapa-boykisser.gif")
parser.add_argument('--output', type=str, help='output', default="out/run-gif.py")
parser.add_argument('--width', type=int, help='Number of characters in a line', default=100)
parser.add_argument('--template', type=str, help='Template of the code, must have #INJECT comment for frames var injection point', default="src/gif-runner.py")
args = parser.parse_args()

frames=[]
im = Image.open(args.input)

for frame in ImageSequence.Iterator(im):


    width, height = frame.size
    aspect_ratio = height/width
    new_width = args.width
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
        pixel = struct.pack("BBBc", *color_pixel, pixel.encode())
        new_pixels.append(pixel)    

    new_pixels_count = len(new_pixels)
    ascii_image = [b"".join(new_pixels[index:index + new_width]) for index in range(0, new_pixels_count, new_width)]

    frames.append([frame.info['duration']/1000, ascii_image])

## Debug
# open("temp/raw_frames.txt","w").write(str(frames))

source = open(args.template).read()
open(args.output,'w').write(source.replace("#INJECT", f"a={str(frames)}", 1))
