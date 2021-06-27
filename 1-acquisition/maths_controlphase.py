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
import statistics
import csv
import os.path

#==============================================
# experiment parameters
#==============================================
par = input('Participant: ')

num_level           = 3 # Low, Mild, Higher
num_block           = 4 # num block per level
num_break           = num_block - 1
block_time          = 50 # in seconds
block_break         = 20 # in seconds
#block_fixation_time = 10  # inter trial interval, i.e., how long the fixation will stay in second

experiment_time = num_level * ((num_block * block_time) + (num_break * block_break))
print(f"Total experiment time = {'{:.2f}'.format(experiment_time/60)} Minute" )
      
#==============================================
# Configuration 
#==============================================
levels = ['LowStress', 'MildStress', 'HigherStress']

#name, type, channel_count, sampling rate, channel format, source_id
#info = StreamInfo('CytonMarkers', 'Markers', 1, 0.0, 'int32', 'CytonMarkerID')#make an outlet
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
        print(operant1, operator1, operant2, operator2, operant3)
        ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}')
        corr_ans = ans
        if (type(corr_ans) == int) and (0 <= corr_ans) and (corr_ans <= 9):
            corr_ans = int(corr_ans)
            print("Type after if else:", type(corr_ans))
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.draw()
            mywin.flip()
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
            message.draw()
            mywin.flip()
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
        print(operant1,operator1,operant2, operator2,operant3,operator3,operant4)
        try:
            ans = eval(f'{operant1}{operator1}{operant2}{operator2}{operant3}{operator3}{operant4}')
            if type(ans) == int and 0 <= ans <=9:
                corr_ans = ans
                message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2} {operator2} {operant3} {operator3} {operant4}', languageStyle='LTR')
                message.contrast =  0.3
                message.height= 0.2
                message.draw() 
                mywin.flip()   
                return corr_ans  
            else: 
                return drawMaths(level)
        except ZeroDivisionError:
            return drawMaths(level)

def drawAnswer(corr_ans, ans):
    print(type(corr_ans),type(ans))
    if ans.isdigit() and corr_ans == int(ans):
        message_ = "Correct!"
        print(message_)
    elif ans.isdigit() and corr_ans != int(ans):
        message_ = "Incorrect!"
        print(message_)
    else:
        message_ = "An integer between 0-9 is required."
    message = visual.TextStim( mywin, text=message_, languageStyle='LTR')
    message.contrast =  0.3
    message.height= 0.07
    message.draw() # draw on screen
    mywin.flip()   # refresh to show what we have draw      

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
    core.wait(fixationTime)
    drawTextOnScreen('')

# mywin = visual.Window([640, 360], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode
mywin = visual.Window([1366, 768], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode

drawTextOnScreen('Loading...')
core.wait(3)
     
###############################  Control Phase ##################################
# to calculate ave time taken to answer for each stress level
avg_times = {level: [] for level in levels}
print(avg_times)
while True:
    isTrianing = True
    drawTextOnScreen('Training session\nPlease wait\nPress space bar to start')
    keys = event.getKeys()
    if 'space' in keys:      # If space has been pushed
        drawTextOnScreen('') 
        for level in levels:
            drawTextOnScreen(f'Examples of {level}')
            core.wait(1)
            block_ = 0
            # do for 5 mins
            while block_ < num_block:
                drawTextOnScreen(f'Block {block_ + 1}')
                core.wait(1)
                timeout_start = time.time()
                while time.time() < timeout_start + block_time:
                    #Questions
                    start_eachq = time.time()
                    corr_ans = drawMaths(level)
                    print(f"Correct answer: {corr_ans}")
                    
                    #Answer
                    answers = event.waitKeys()
                    print(f"User's answer: {answers}")
                    while ('1' not in answers) and ('2' not in answers) and ('3' not in answers) and ('4' not in answers):
                        print("ans not 1-4")
                        answers = event.waitKeys()

                    stop_eachq  = time.time()
                    ans_time = stop_eachq - start_eachq
                    avg_times[level].append(ans_time)
                    print(f"User's answer time: {ans_time}")
                block_ += 1
                drawFixation( block_break)
            drawFixation(block_break)
        avg_low = statistics.mean(avg_times['LowStress']) * 0.9
        avg_mild = statistics.mean(avg_times['MildStress']) * 0.9
        avg_higher = statistics.mean(avg_times['HigherStress']) * 0.9
        
        try:
            os.makedirs('Maths')
        except:
            pass
        filename = "Maths/participants_maths_time.csv"
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(f"Maths/participants_maths_time.csv", mode) as myfile:
            fileEmpty = os.stat(filename).st_size == 0
            headers = ['Participant','LowStress' , 'MildStress', 'HigherStress']
            writer = csv.DictWriter(myfile, delimiter=',', lineterminator='\n',fieldnames=headers)
            if fileEmpty:
                writer.writeheader()  # file doesn't exist yet, write a header
            writer.writerow({'Participant': par, 'LowStress': avg_low, 'MildStress': avg_mild, 'HigherStress': avg_higher})
            # myfile.write("\n")

        drawTextOnScreen('End of Training Session')
        core.wait(1)
        drawTextOnScreen('Press space bar to end')
        _ = event.waitKeys()
        isTrianing = False
        break

mywin.close()
core.quit()