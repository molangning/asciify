#!/bin/python3

# Readable version
# search for space in front to put the unpacker first, then the back.
#
# TODO change to allow user to input pattern 

import re
import lzma
import base64
import argparse
from PIL import Image,ImageOps,ImageStat

parser = argparse.ArgumentParser(description='Converts given code into the shape of input picture')
parser.add_argument('--image', type=str, help='input image', default="sample_media/frame-7.jpg")
parser.add_argument('--code', type=str, help='python file of code', default="out/run-gif.py")
parser.add_argument('--output', type=str, help='output', default="out/formatted-code.py")
parser.add_argument('--width', type=int, help='Number of characters in a line', default=400)
args = parser.parse_args()

code = open(args.code).read()
og_img = Image.open(args.image)

def asciify(img, new_width = args.width):

    width, height = img.size
    aspect_ratio = height/width
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img_grayscale = img.convert('L')

    if ImageStat.Stat(img_grayscale).mean[0] > 128:
        img_grayscale = ImageOps.invert(img).convert('L')


    chars = ["#", "?", ":", " "]

    pixels = img_grayscale.getdata()

    new_pixels = []
    for pixel in pixels:
        new_pixels.append(chars[pixel // 64])

    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)

    # One liner to return list with each line representing a row of ascii characters

    return [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]

def count_usable(to_count):
    result = re.sub(r"[^#?]+", "", to_count)
    return len(result)

text = asciify(og_img)
usable_chars = ["#", "?"]

unpacker_head = r'import base64,lzma;exec(lzma.decompress(base64.b64decode("""'
unpacker_end = '""")))'

unpacker_end_length = len(unpacker_end)
unpacker_head_length = len(unpacker_head)

# shebang is for linux, the correct execution is python3 file.py
# but it's there if it's called directly
file_magic = "#!/bin/python3\n\n"

if len(unpacker_head) > count_usable(text[0]):
    raise Exception(f"unpacker head is longer than the amount of free continuous space in the first line, minimum width is {len(unpacker_head)}")


line_width = len(text[0])

target_inject = text[-1][line_width - unpacker_end_length:]

if len(target_inject) > count_usable(target_inject):
    raise Exception("unpacker end is longer than the amount of free continuous space in the last line")

text="\n".join(text)
# print(text)

max_payload_size = count_usable(text[unpacker_head_length:len(text) - unpacker_end_length])
payload = base64.b64encode(lzma.compress(code.strip().encode())).decode()

if len(payload) > max_payload_size:

    print("Calculating resize...")

    while True:

        new_payload_len = 0

        new_width += 1
        new_height = int(aspect_ratio * new_width * 0.55)
        
        img = img.resize((new_width, new_height))
        img_grayscale = img.convert('L')

        if ImageStat.Stat(img_grayscale).mean[0] > 128:
            img_grayscale = ImageOps.invert(img).convert('L')

        new_pixels = []

        for pixel in img_grayscale.getdata():
            new_pixels.append(chars[pixel//128])

        new_payload_len = ''.join(new_pixels).count("#")

        if new_payload_len >= len(payload):
            break

    print(f"Found nearest width {new_width+1}, try using it as width")

    raise Exception(f"payload is longer than the amount of free space we have ({len(payload)} > {max_payload_size})")

print("Packed payload")

payload_pointer = 0
text_pointer = 0

output=""
for i in text[unpacker_head_length:len(text) - unpacker_end_length]:
    text_pointer += 1

    if payload_pointer > len(payload) - 1:
        output+=text[unpacker_head_length + text_pointer - 1:len(text) - unpacker_end_length]
        break

    if i in usable_chars:
        output += payload[payload_pointer]
        payload_pointer += 1
        continue

    output += i


if payload_pointer != len(payload):
    raise Exception(f"Unused payload left over {payload_pointer} != {len(payload)}")

output = file_magic + unpacker_head + output + unpacker_end

open(args.output, "w").write(output)

print(f"Generated file at {args.output}")