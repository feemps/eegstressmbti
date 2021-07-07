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
import csv
import os.path

#==============================================
# experiment parameters
#==============================================
par = input('Participant: ')
LowStress = input('LowStress time: ')
MildStress = input('MildStress time: ')
HigherStress = input('HigherStress time: ')

avg_times = { 
    'LowStress' : LowStress,
    'MildStress' : MildStress,
    'HigherStress' : HigherStress,
}

num_level           = 3 # Low, Mild, Higher
num_block           = 4 # num block per level
num_break           = num_block - 1
block_time          = 40 # in seconds
block_break         = 10 # in seconds

experiment_time = num_level * ((num_block * block_time) + (num_break * block_break))
print(f"Total experiment time = {'{:.2f}'.format(experiment_time/60)} Minute" )
      

#==============================================
# Configuration 
#==============================================
levels = ['LowStress', 'MildStress', 'HigherStress']

info = pylsl.StreamInfo('CytonMarkers', 'Markers', 1, 0.0, 'string', 'CytonMarkerID')#make an outlet
outlet = pylsl.StreamOutlet(info)
# %whos

operators_low = ['+', '-']
operators_mild = ['+', '-', '*']
operators_higher = ['+', '-', '*', '/']

def drawMaths(level):
    if level == "LowStress":
        operant1 = random.randint(0,9)
        operant2 = random.randint(0,9)
        operant3 = random.randint(0,9)
        operator1 = random.choice(operators_low)
        operator2 = random.choice(operators_low)
        # print(operant1, operator1, operant2, operator2, operant3)
        ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}')
        corr_ans = ans
        if (type(corr_ans) == int) and (0 <= corr_ans) and (corr_ans <= 9):
            corr_ans = int(corr_ans)
            # print("Type after if else:", type(corr_ans))
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw
            eegMarking('math', level, 'start')
            return corr_ans      
        else: 
            return drawMaths(level)

    elif level == "MildStress":
        operant1 = random.randint(0,99)
        operant2 = random.randint(0,99)
        operant3 = random.randint(0,99)
        operator1 = random.choice(operators_mild)
        operator2 = random.choice(operators_mild)
        #print(operant1,operator1,operant2, operator2,operant3)
        ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}')
        if type(ans) == int and 0 <= ans <=9:
            corr_ans = ans
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height= 0.2
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw
            eegMarking('math', level, 'start')
            return corr_ans      
        else: 
            return drawMaths(level)
 
    else :
        operant1 = random.randint(0,99)
        operant2 = random.randint(0,99)
        operant3 = random.randint(0,99)
        operant4 = random.randint(0,99)
        operator1 = random.choice(operators_higher)
        operator2 = random.choice(operators_higher)
        operator3 = random.choice(operators_higher)
        # print(operant1,operator1,operant2, operator2,operant3,operator3,operant4)
        try:
            ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}{operator3}{operant4}')
            if type(ans) == int and 0 <= ans <=9:
                corr_ans = ans
                message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3} {operator3} {operant4}', languageStyle='LTR')
                message.contrast =  0.3
                message.height= 0.2
                message.draw() # draw on screen
                mywin.flip()   # refresh to show what we have draw
                eegMarking('math', level, 'start')
                return corr_ans  
            else: 
                return drawMaths(level)
        except ZeroDivisionError:
            return drawMaths(level)

def drawAnswer(corr_ans, ans):
    if (ans!='num_1') and (ans!='num_2') and (ans!='num_3') and (ans!='num_4') and (ans!='num_5') and (ans!='num_6') and (ans!='num_7') and (ans!='num_8') and (ans!='num_9') and (ans!='num_0'): 
        marking = "O"
        message_ = "An integer between 1-4 is required."
        # print(message_)
    elif corr_ans == int(ans[-1]):
        message_ = "CORRECT!"
        marking = "T"
        # print(message_)
    else:
        message_ = "INCORRECT!"
        marking = "F"
        # print(message_)
    eegMarking('math', level, marking)
    message = visual.TextStim( mywin, text=message_, languageStyle='LTR')
    message.contrast =  0.3
    message.height= 0.07
    message.draw() # draw on screen
    mywin.flip()   # refresh to show what we have draw
    return marking

def drawTextOnScreen(massage) :
    message = visual.TextStim( mywin, text=massage, languageStyle='LTR')
    message.contrast =  0.3
    message.height= 0.07
    message.draw() # draw on screen
    mywin.flip()   # refresh to show what we have draw
    
def drawFixation(fixationTime):
    fixation = visual.ShapeStim(mywin,
                                vertices=((0, -0.5), (0, 0.5), (0,0), (-0.5,0), (0.5, 0)),
                                lineWidth=5,
                                closeShape=False,
                                lineColor="white"
            )
    fixation.draw()
    mywin.flip()   # refresh to show what we have draw
    eegMarking(stampType =  "fixation" )
    core.wait(fixationTime)
    drawTextOnScreen('')
     
def eegMarking(stampType, level=None, marking=None):   # use trial variable from main
    markerString = str(stampType) + "," + str(level) + "," + str(marking)
    markerString = str(markerString)                              
    print("Marker : {}".format(markerString))
    outlet.push_sample([markerString])

mywin = visual.Window([1920, 1080], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode

# drawTextOnScreen('Loading...')
# core.wait(3)
     
###############################  Stress Phase ##################################
# use the avg time from the control phase for time limit

while True:
    drawTextOnScreen('Stress session\nPlease wait\nPress ENTER to start')
    keys = event.getKeys()
    if 'num_enter' in keys:      # If space has been pushed
        print("="*51)
        print(f"====== PAR {par} | START MATH STRESS SESSION ======")
        print("="*51)
        drawTextOnScreen('') 
        for idx,level in enumerate(levels) : # for each level
            drawTextOnScreen(f'Level {idx+1}')
            core.wait(1)
            block_ = 0
            while block_ < num_block:
                drawTextOnScreen(f'Block {block_ + 1}/4')
                core.wait(1)
                timeout_start = time.time()
                while time.time() < timeout_start + block_time:
                    corr_ans = drawMaths(level)
                    # print(f"Correct answer: {corr_ans}")

                    answers = event.waitKeys(maxWait = float(avg_times[level]))
                    # print(f"User's answer: {type(answers)}")
                    if answers is None:
                        marking = "S"
                        eegMarking('math', level, marking)
                        message_ = 'Too slow!'
                        drawTextOnScreen(message_)
                        core.wait(0.5)
                    else:
                        marking = drawAnswer(corr_ans, answers[0])
                        core.wait(0.5)
                    print("="*10)

                block_ += 1
                drawFixation(block_break)

            # time for questionaire at the end of the level
            drawTextOnScreen('Questionnaire')
            core.wait(60)
            if idx != 2:
                drawTextOnScreen('Please prepare for next level')
                core.wait(3)

        drawTextOnScreen('End of Stress Session\nPress ENTER to end')
        _ = event.waitKeys()
        break

mywin.close()
core.quit()
print("="*51)
print(f"====== PAR {par} | MATH STRESS SESSION ENDED ======")
print("="*51)
