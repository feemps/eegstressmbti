import random
import pylsl
import numpy as np
import pandas as pd
import time
import itertools
import math
import psychopy 
from psychopy import visual, core, event
from datetime import datetime
from IPython.display import clear_output
import random
from numpy.random import default_rng
import operator

operators_low = ['+', '-']
operators_mild = ['+', '-', '*']
operators_higher = ['+', '-', '*', '/']

def drawMaths(level):
    if level == "low":
        operant1 = random.randint(0,9)
        operant2 = random.randint(0,9)
        operant3 = random.randint(0,9)
        operator1 = random.choice(operators_low)
        operator2 = random.choice(operators_low)
        #print(operant1,operator1,operant2, operator2,operant3)
        ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}')
        if type(ans) == int and 0 <= ans <=9:
            #print(ans)
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height= 0.5
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw
            #eegMarking()     
        else: 
            drawMaths(level)

    if level == "mild":
        operant1 = random.randint(0,99)
        operant2 = random.randint(0,99)
        operant3 = random.randint(0,99)
        operator1 = random.choice(operators_mild)
        operator2 = random.choice(operators_mild)
        #print(operant1,operator1,operant2, operator2,operant3)
        ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}')
        if type(ans) == int and 0 <= ans <=9:
            #print(ans)
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height= 0.5
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw
            #eegMarking()     
        else: 
            drawMaths(level)

    if level == "higher":
        operant1 = random.randint(0,99)
        operant2 = random.randint(0,99)
        operant3 = random.randint(0,99)
        operator1 = random.choice(operators_higher)
        operator2 = random.choice(operators_higher)
        #print(operant1,operator1,operant2, operator2,operant3)
        try:
            ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}')
            if type(ans) == int and 0 <= ans <=9:
                #print(ans)
                message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3}', languageStyle='LTR')
                message.contrast =  0.3
                message.height= 0.5
                message.draw() # draw on screen
                mywin.flip()   # refresh to show what we have draw
                #eegMarking()     
            else: 
                drawMaths(level)
        except ZeroDivisionError:
            drawMaths(level)

for i in range(5):
    print("#########")
    drawMaths('higher')