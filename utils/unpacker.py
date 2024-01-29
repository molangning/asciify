#!/usr/bin/python3

# b.replace(".",'').replace("@",'').replace('\n','').replace('\r','').replace('\r\n','')   -> 82 char
# re.sub(r"\.|@|(\r\n|\r|\n)","",b) -> 29

def unpacker(chars):
    # v1 unpacker
    import base64,lzma,re
    code=re.sub(r"\.|@|(\r\n|\r|\n)","",chars)
    compressed_code=base64.b64decode(chars)
    code=lzma.decompress(compressed_code)
    exec(code)
    

# Minified version

def a(b):
    # v1 unpacker
    import base64,lzma,re
    print(lzma.decompress(base64.b64decode(re.sub(r"\.|@|(\r\n|\r|\n)","",b)))) # 39 chars

compressed_text = open("temp/compressed.txt").read()
unpacker(compressed_text)