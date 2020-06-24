# Generated with SMOP  0.41
from libsmop import *


# clipValue.m


def clipValue(val=None, valMin=None, valMax=None):
    # check if value is valid

    for i in arange(1, size(ravel(val)), 1).reshape(-1):
        if val(i) < valMin:
            val[i] = valMin
        # clipValue.m:11
        else:
            if val(i) > valMax:
                val[i] = valMax
# clipValue.m:15
