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

#==============================================
# experiment parameters
#==============================================
combination         = 3
task                = 2
classes             = combination * task
num_trial_per_block = 5
num_block           = 4
num_trial           = num_trial_per_block * num_block
total_data_point    = classes * num_trial 
block_time          = 40
block_break         = 30

stim_time           = 2
stim_imagery        = 2
stim_blink_time     = 0
task_fixation_time = (0.8, 1.2)
trial_fixation_time= 2
block_fixation_time = 10  # inter trial interval, i.e., how long the fixation will stay in second


experiment_time  = ( trial_fixation_time + stim_time + stim_imagery + task_fixation_time[-1] ) * combination * num_trial
print(f"Total experiment time = {'{:.2f}'.format(experiment_time/60)} Minute" )
      
    
#==============================================
# Configuration 
#==============================================
levels = ['LowStress', 'MildStress', 'HigherStress']
levels = ['LowStress']
#name, type, channel_count, sampling rate, channel format, source_id
#info = StreamInfo('CytonMarkers', 'Markers', 1, 0.0, 'int32', 'CytonMarkerID')#make an outlet
info = pylsl.StreamInfo('CytonMarkers', 'Markers', 1, 0.0, 'string', 'CytonMarkerID')#make an outlet
outlet = pylsl.StreamOutlet(info)
# %whos

stims = {
    '1': [1, 2, 3],
    '2': [2, 1, 3],
    '3': [3, 2, 1],
}

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
            message.height = 0.3
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw
            #eegMarking()
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
            message.height= 0.3
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw
            #eegMarking()
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
                message.height= 0.3
                message.draw() # draw on screen
                mywin.flip()   # refresh to show what we have draw
                #eegMarking()
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

def drawTrial( idx_mark, type_mark, stimTime ) :
    drawTextOnScreen('') 
    core.wait(stim_blink_time)
    if type_mark == 'imagery':
        load_img = blank
    else:
        load_img = all_img[idx_mark]    
    load_img.draw()
    mywin.flip()
    eegMarking("img_stim", idx_mark, type_mark)
    core.wait(stimTime)
    
def drawFixation(fileName, fixationTime):
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
     
def eegMarking(stampType, idx_mark=None, type_mark=None):   # use trial variable from main
    if not isTrianing :
        if stampType == "img_stim" :
            markerString = str(block+1) + "," + str(trial+1) + ","  + str(idx_mark+1) + "," + str(type_mark) + "," + str(stampType)
        elif stampType == "fixation" :
            markerString = str(block+1) + "," + str(trial+1) + "," + str("Fixation")
    else:
        markerString = 'Training'
    markerString= str(markerString)                              
    print("Marker string {}".format(markerString))
    outlet.push_sample([markerString])


#trial_idx = input()

wait = 1

    
# mywin = visual.Window([1366, 768], color='black', fullscr=True, screen=1, units='norm')     # set the screen and full screen mode
# mywin = visual.Window([640, 360], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode
mywin = visual.Window([1366, 768], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode

drawTextOnScreen('Loading...')
core.wait(3)
     

###############################  Control Phase ##################################
# to calculate ave time taken to answer for each stress level
ave_times = {level: [] for level in levels}

while True:
    isTrianing = True
    drawTextOnScreen('Training session\nPlease wait\nPress space bar to start')
    keys = event.getKeys()
    if 'space' in keys:      # If space has been pushed
        drawTextOnScreen('') 
        for i,level in enumerate(levels):
            drawTextOnScreen(f'Examples of {levels[i]}')
            core.wait(wait)
            timeout_start = time.time()
            block_ = 0
            # do for 5 mins
            if block_ <= num_block:
                print(block_)
                while time.time() < timeout_start + block_time:
                    #Questions
                    start_eachq = time.time()
                    corr_ans = drawMaths(level)
                    print(f"Correct answer: {corr_ans}")
                    
                    #Answer
                    answers = event.waitKeys()
                    print(f"User's answer: {answers}")
                    #if len(answers) == 0:
                        #drawTextOnScreen(f'Too slow')
                        #core.wait(3)
                    #else:
                    stop_eachq  = time.time()
                    ans_time = stop_eachq - start_eachq
                    ave_times[level].append(ans_time)
                    print(f"User's answer time: {ans_time}")
                    #drawAnswer(corr_ans, answers[0])
                block_ += 1
                drawFixation('task break', block_break)

        drawTextOnScreen('End of training session')
        core.wait(1)
        drawTextOnScreen('Press space bar to continue')
        _ = event.waitKeys()
        isTrianing = False
        break

################
####### Experiment session
play = True
while play:
    drawTextOnScreen('Experiment session : Press space bar to start')
    keys = event.getKeys()
    if 'space' in keys:      # If space has been pushed
        start = time.time()
        drawTextOnScreen('') 

        for block in range(num_block) :
            
            if block != 0:
                drawTextOnScreen('RELAX TIME\n*Do not remove your head set\nPress space bar to continue')
                _ = event.waitKeys()

            drawTextOnScreen(f'Ready\n Block {block+1} / {num_block}')
            core.wait(2)                
            for trial in range(num_trial_per_block):
                for img in fname:
                    drawTextOnScreen(f'Trial {trial+1}/{num_trial_per_block}')
                    core.wait(wait)
                    clear_output(wait=True)
                    drawFixation('trial break', trial_fixation_time-wait)

                    #Perception
                    drawTrial(img-1, 'perception', stim_time)   # drawTrail(idx_mark, type_mark, stimTime)
                    drawFixation('task break', np.random.uniform(task_fixation_time[0], task_fixation_time[1]))
                    #Imagery
                    drawTrial(img-1, 'imagery', stim_time)

        drawTextOnScreen('End of experiment, Thank you')
        stop  = time.time()
        print(f"Total experiment time = {(stop-start)/60} ")
        core.wait(10)
        play = False

mywin.close()
core.quit()