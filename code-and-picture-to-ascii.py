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

import base64,lzma,re

unpacker_head=r'import base64,lzma,re;exec(lzma.decompress(base64.b64decode(re.sub(r"\.|#|(\r\n|\r|\n)","","""'


unpacker_end='"""))))'
unpacker_end_length=len(unpacker_end)
unpacker_head_length=len(unpacker_head)

text = open("ascii_image.txt").read()
code = open("run-gif.py").read()
# file magic is for linux, the correct execution is python3 file.py
# but it's there for direct executioners
file_magic="#!/bin/python3\n\n"

text=text.split('\n')
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


output=unpacker_head+output+unpacker_end+"#"*(offset-unpacker_end_length)

open("temp.txt","w").write(output)