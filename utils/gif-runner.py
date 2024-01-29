#!/bin/python3

import json,base64,time,lzma

data = lzma.decompress(base64.b64decode())

frames = json.loads(data)

while True:
    for i in frames:
        print("\x1B[2J\x1B[H"+i[1])  
        time.sleep(i[0])