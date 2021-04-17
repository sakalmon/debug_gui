import os
from os.path import isfile
from os.path import join


for f in os.listdir():
    if isfile(join(os.getcwd(), f)):
        print(f)