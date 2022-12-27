import copy
import sys
import pygame
import random
import numpy as np
import time

case = int(input('Enter choice: '))
if case == 3:
    try:
        execfile("3x3.py")
    except NameError:
        exec(open("3x3.py").read())

elif case == 5:
    try:
        execfile("5x5.py")
    except NameError:
        exec(open("5x5.py").read())