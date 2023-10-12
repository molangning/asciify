#!/usr/bin/python3

# shamelessly taken from https://jagt.github.io/python-single-line-convert/
# 'Reindent based on first line's indent' will reindent -8 spaces in this case
# comments are still kept at this moment
from datetime import datetime
def foo():
    """
    triple double quotes are ignored
    or are they? 
    """
    return '"Hey kid what time is it?"'


# done
print( foo() + '''\n\t'''    \
            + str(datetime.now()))
try:
    raise RuntimeError()
except:
    pass
    """
    ONE MORE TIME
    For good measures
    """
