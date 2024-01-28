#!/bin/python3

# Readable version
# search for space in front to put the unpacker first, then the back.
#
# TODO change to allow user to input pattern 
#
# packer v1
# import base64,lzma,re
# base64.b64encode(lzma.compress(bytes(re.sub(r"(\r\n|\r|\n){2,}","\n",re.sub(r"\s*\"\"\".*?\"\"\"|\s+\\\s*|#.*?(\r\n|\r|\n)","",b,0,re.S)).strip(),"utf-8")))
#
# """b""" contains the ascii art
# header and footer refers to the amount of continuous space needed to execute properly
#
# unpacker method 1
# import base64,lzma,re;exec(lzma.decompress(base64.b64decode(re.sub(r"\.|@|(\r\n|\r|\n)","","""b""")))) -> header 90 char, footer 7 char
#
# unpacker method 2, not working due to regex replacing the . in function calls
# import re;re.sub(r"\.|@|(\r\n|\r|\n)","","""exec("import base64,lzma;exec(lzma.decompress(base64.b64decode('b')))"))""") -> header 40 char, footer 4 char
#

import base64,lzma,re,sys,argparse
import argparse
from PIL import Image,ImageOps,ImageStat

parser = argparse.ArgumentParser(description='Coverts given code into the shape of input picture')
parser.add_argument('--image', type=str, help='input image', default="sample_media/boykisser.jpg")
parser.add_argument('--code', type=str, help='python file of code', default="run-gif.py")
parser.add_argument('--output', type=str, help='output', default="animated-boykisser.py")
parser.add_argument('--width', type=int, help='Number of characters in a line', default=400)
args = parser.parse_args()

img_name=args.image
code=open(args.code).read()
img=Image.open(img_name)

width, height = img.size
aspect_ratio = height/width
new_width = args.width
new_height = aspect_ratio * new_width * 0.55
img = img.resize((new_width, int(new_height)))

img_grayscale = img.convert('L')

if ImageStat.Stat(img_grayscale).mean[0] > 128:
    img_grayscale = ImageOps.invert(img).convert('L')


chars = ["#", "."]

pixels = img_grayscale.getdata()

new_pixels = []
for pixel in pixels:
    new_pixels.append(chars[pixel//128])

new_pixels = ''.join(new_pixels)
new_pixels_count = len(new_pixels)
text = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]

    


unpacker_head=r'import base64,lzma,re;exec(lzma.decompress(base64.b64decode(re.sub(r"\.|#|(\r\n|\r|\n)","","""'


unpacker_end='"""))))'
unpacker_end_length=len(unpacker_end)
unpacker_head_length=len(unpacker_head)


# file magic is for linux, the correct execution is python3 file.py
# but it's there for direct executioners
file_magic="#!/bin/python3\n\n"

width = len(text[0])



counter=0
for i in text[0]:
    if i == "#":
        counter+=1

if len(unpacker_head) > counter:
    raise Exception("unpacker head is longer than the amount of free continuous space in the first line")

start_line=unpacker_head+text[0][unpacker_head_length]


counter=0
offset=1
found_offset=False

last_line=text[-1]
# reverse last line
for i in last_line[::-1]:
    if i == "#":
        counter+=1
    else:
        counter=0
    if counter == unpacker_end_length:
        found_offset=True
        break
    offset+=1


else:
    raise Exception("unpacker end is longer than the amount of free continuous space in the last line")


max_payload_size=(width-unpacker_head_length)+((len(text)-2)*width)+(len(last_line)-offset)

payload=base64.b64encode(lzma.compress(bytes(re.sub(r"(\r\n|\r|\n){2,}","\n",re.sub(r'\s*""".*?"""|\s+\\\s*|#.*?(\r\n|\r|\n)',"",code,0,re.S)).strip(),"utf-8"))).decode("utf-8")
# print("\n".join(text))
if len(payload)>max_payload_size:
    raise Exception("payload is longer than the amount of free space")

text="\n".join(text)

output=""
for i in text[unpacker_head_length:len(text)-offset]:
    if len(payload) > 0:
        if i == "#":
            output+=payload[0]
            payload=payload[1:]
            continue
    output+=i


output=file_magic+unpacker_head+output+unpacker_end+"#"*(offset-unpacker_end_length)

open(args.output,"w").write(output)

print(f"Generated file at {args.output}")