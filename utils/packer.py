#!/usr/bin/python3
# replace indentation with a space
# actually how do we even detect an indentation?
# TODO add dynamic detection
# how to fix: detect smallest continuous blocks of spaces in front of each code
# then replace accordingly
# eg. four spaces -> one block
# eight spaces -> two block
# TODO change back and implement detection with /t
# warn if mix tabs and space?
# TODO actually do all of these and not give up due to the resulting code taking 
# up more space that you thought it will

# import base64;base64.b64encode(b"a") --> 36 char
# import base64 as a;a.b64encode(b"a") --> 36 char
# 
# second line may be more character saving for 
# multiple calls

#
# bytes("hello\3\\n","utf-8") --> 25 char
# "hello\3\\n".encode("utf-8") --> 26 char
#


test1="""
 
a=1
b=2
# line comment
if a==1: # after line comment
 if b==2:
  print("a=1,b=1")
  """

test2="""a=1
b=2
# line comment
if a==1: # after line comment
    if b==2:
        print("a=1,b=1")
"""

test3="""a=1
b=2
# line comment
if a==1: # after line comment
\tif b==2:
\t\tprint("a=1,b=1")
"""


# regex to detect comments: #.*
# I know the compiled code will be so unreadable and unmaintainable
#
# this regex is cursed
# (?s)^\s*\"\"\".*?\"\"\"
#
# Plain english: match everything, including the newline character as long as it start with spaces or none at all. 
# Return as soon as you found the end of a triple quote
# I need bleach for this
#
# BUT WAIT WE AREN'T DONE
# I COMBINED THEM
# AND NOW
#
# (?s)^\s*\"\"\".*?\"\"\"|#.*?(\r\n|\r|\n)
# AAIFOiuubaOIajnfsKANDLANF cursed regex
#
def packer(code):
    # v1 packer
    import base64, re, lzma
    
    # removes doc strings, comments and multiline splits
    code=re.sub(r'\s*""".*?"""|\s+\\\s*|#.*?(\r\n|\r|\n)','',code,0,re.S)
    # removes excess newlines
    code=re.sub(r"(\r\n|\r|\n){2,}","\n",code)
    # removes trailing spaces
    code=code.strip()

    # print(bytes(code,"utf-8"))
    compressed_code=lzma.compress(bytes(code,"utf-8"))
    encoded_code=base64.b64encode(compressed_code)
    return encoded_code

# and now for the unholy amalgamation
# the fact that this exists means that god is not omnipotent
# or god is ignorant
# kudos if you get the reference from that one youtube video
#

def packed_packer(b):
    # v1 packer
    import base64,re,lzma
    # what have I done....
    # there is a very fine line between obfuscation and optimization
    # and it appears that I have blurred them a bit too much
    # 
    return base64.b64encode(lzma.compress(bytes(re.sub(r"(\r\n|\r|\n){2,}","\n",re.sub(r'\s*""".*?"""|\s+\\\s*|#.*?(\r\n|\r|\n)',"",b,0,re.S)).strip(),"utf-8")))

# print(packer(test3))
# print(a(test3))

temp = "#inject some comments"

print(packer(open("example.py").read()))
print(packed_packer(open("example.py").read())) 

