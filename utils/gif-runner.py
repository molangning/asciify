#!/bin/python3

import json,time,struct

# Yeah yeah it's unsafe, but it's an handy debug tool
frames = eval(open("temp/raw_frames.txt").read())#INJECT

print("load done")

unpacked_frames = []

for frame in frames:

    finished_frame = []

    for line in frame[1]:

        finished_line = ""
        line = [line[pos:pos+4] for pos in range(0,len(line),4)]

        for pixel in line:
            *color, ascii_char = struct.unpack("BBBc", pixel)
            finished_line += "\x1b[38;2;%i;%i;%im%s\x1b[0m" % (*color, ascii_char.decode())

        finished_frame.append(finished_line)

    finished_frame = "\n".join(finished_frame)

    unpacked_frames.append([frame[0], "\x1B[2J\x1B[H"+finished_frame])

print("Parse done")

while True:
    for i in unpacked_frames:
        print(i[1])
        time.sleep(i[0])
