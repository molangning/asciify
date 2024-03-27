# asciify

Asciify turns your code or gifs into ascii characters that is terminal printable.

`gif-to-code.py` converts your gif into pure, unformatted code that displays your gif in your terminal with the help of ansi escape codes.

`code-and-picture-to-ascii.py` takes a code and reference image and formats the code into the shape of the image.

# Caveats

1. Code has to be packed, so it will look like some random characters. It won't be like c ascii art as python does not have it's single line code and multiline comments functionalities.

2. The run gif code is slow as it has to unpack the code, there can be some optimizations done, but I am out of ideas.

# Demos!

![Chipi](sample_media/chipi-demo.gif)
