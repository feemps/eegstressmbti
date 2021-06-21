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
num_block           = 15
num_trial           = num_trial_per_block * num_block
total_data_point    = classes * num_trial 

stim_time           = 2
stim_imagery        = 2
stim_blink_time     = 0
task_flixation_time = (0.8, 1.2)
trial_flixation_time= 2
block_fixation_time = 10  # inter trial interval, i.e., how long the fixation will stay in second


experiment_time  = ( trial_flixation_time + stim_time + stim_imagery + task_flixation_time[-1] ) * combination * num_trial
print(f"Total experiment time = {'{:.2f}'.format(experiment_time/60)} Minute" )
      
    
#==============================================
# Configuration 
#==============================================
levels = ['LowStress', 'MildStress', 'HigherStress']
# levels = ['HigherStress']
#name, type, channel_count, sampling rate, channel format, source_id
#info = StreamInfo('CytonMarkers', 'Markers', 1, 0.0, 'int32', 'CytonMarkerID')#make an outlet
info = pylsl.StreamInfo('CytonMarkers', 'Markers', 1, 0.0, 'string', 'CytonMarkerID')#make an outlet
outlet = pylsl.StreamOutlet(info)
# %whos

color = {'Red':(255, 0, 0),
        'Green':(0, 255, 0),
        'Blue':(0, 0, 255),
        'Purple' : (148,0,211),
        'Orange': (255,165,0),
        'Yellow' :(255,255,0),
        }

word = ['Red', 'Green', 'Blue', 'Purple', 'Orange', 'Yellow']


def drawMaths(level):
    if level == "LowStress":

        idxs = np.random.choice(6, 3, replace=False)

        word_1 = word[idxs[0]]
        word_2 = word[idxs[1]]
        word_3 = word[idxs[2]]
        word_4 = None

        color_1 = color[word_1]
        color_2 = color[word_2]
        color_3 = color[word_3]
        color_4 = None

        message = visual.TextStim( mywin, text=f'{word_1}\t', languageStyle='LTR')
        message.contrast =  0.3
        message.height = 0.2
        message.colorSpace = 'rgb255'
        message.color = color_1
        message.pos = (-0.5, 0)
        message.draw() # draw on screen

        message = visual.TextStim( mywin, text=f'{word_2}\t', languageStyle='LTR')
        message.contrast =  0.3
        message.height = 0.2
        message.colorSpace = 'rgb255'
        message.color = color_2
        message.pos = (0, 0)
        message.draw() # draw on screen

        message = visual.TextStim( mywin, text=f'{word_3}', languageStyle='LTR')
        message.contrast =  0.3
        message.height = 0.2
        message.colorSpace = 'rgb255'
        message.color = color_3
        message.pos = (0.5, 0)
        message.draw() # draw on screen

        mywin.flip()   # refresh to show what we have draw
        return word_1,word_2,word_3,word_4,color_1,color_2,color_3,color_4
              

    elif level == "MildStress":

        idx_word = np.random.choice(6, 3, replace=False)
        idx_color = np.random.choice(6, 3, replace=False)
        
        word_1 = word[idx_word[0]]
        word_2 = word[idx_word[1]]
        word_3 = word[idx_word[2]]
        word_4 = None

        color_1 = color[word[idx_color[0]]]
        color_2 = color[word[idx_color[1]]]
        color_3 = color[word[idx_color[2]]]
        color_4 = None

        if (idx_word[0] != idx_color[0])and (idx_word[1] != idx_color[1]) and (idx_word[2] != idx_color[2]):
            message = visual.TextStim( mywin, text=f'{word_1}\t', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_1
            message.pos = (-0.5, 0)
            message.draw() # draw on screen

            message = visual.TextStim( mywin, text=f'{word_2}\t', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_2
            message.pos = (0, 0)
            message.draw() # draw on screen

            message = visual.TextStim( mywin, text=f'{word_3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_3
            message.pos = (0.5, 0)
            message.draw() # draw on screen

            mywin.flip()   # refresh to show what we have draw
            return word_1,word_2,word_3,word_4,color_1,color_2,color_3,color_4   
        else: 
            return drawMaths(level)
 
    else :
        idx_word = np.random.choice(6, 4, replace=False)
        idx_color = np.random.choice(6, 4, replace=False)
        
        word_1 = word[idx_word[0]]
        word_2 = word[idx_word[1]]
        word_3 = word[idx_word[2]]
        word_4 = word[idx_word[3]]

        color_1 = color[word[idx_color[0]]]
        color_2 = color[word[idx_color[1]]]
        color_3 = color[word[idx_color[2]]]
        color_4 = color[word[idx_color[3]]]

        if (idx_word[0] != idx_color[0])and (idx_word[1] != idx_color[1]) and (idx_word[2] != idx_color[2]) and (idx_word[3] != idx_color[3]):
            message = visual.TextStim( mywin, text=f'{word_1}\t', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_1
            message.pos = (-0.6, 0)
            message.draw() # draw on screen

            message = visual.TextStim( mywin, text=f'{word_2}\t', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_2
            message.pos = (-0.2, 0)
            message.draw() # draw on screen

            message = visual.TextStim( mywin, text=f'{word_3}', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_3
            message.pos = (0.2, 0)
            message.draw() # draw on screen

            message = visual.TextStim( mywin, text=f'{word_4}', languageStyle='LTR')
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = color_4
            message.pos = (0.6, 0)
            message.draw() # draw on screen

            mywin.flip()   # refresh to show what we have draw
            return word_1,word_2,word_3,word_4,color_1,color_2,color_3,color_4   
        else: 
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

#5 mins
timeout = 30
    
# mywin = visual.Window([1366, 768], color='black', fullscr=True, screen=1, units='norm')     # set the screen and full screen mode
# mywin = visual.Window([640, 360], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode
mywin = visual.Window([1366, 768], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode

drawTextOnScreen('Loading...')
core.wait(3)
     
##############
####  Training session
while True:
    isTrianing = True
    drawTextOnScreen('Training session\nPlease wait\nPress space bar to start')
    keys = event.getKeys()
    if 'space' in keys:      # If space has been pushed
        drawTextOnScreen('') 
        for i,level in enumerate(levels):
            drawTextOnScreen(f'Examples of {levels[i]}')
            core.wait(wait)
            # timeout_start = time.time()

            # Level 1: no time limit


            # do for 5 mins
            while time.time() < timeout_start + timeout:
                #Questions
                start_eachq = time.time()
                word_1,word_2,word_3,word_4,color_1,color_2,color_3,color_4 = drawMaths(level)
                print("Word : ", word_1,word_2,word_3,word_4)
                print(f"Color : ", color_1,color_2,color_3,color_4)
                
                #Answer
                #drawTextOnScreen(f'Type in your answer')
                answers = event.waitKeys()
                print(answers)
                if len(answers) == 0:
                    drawTextOnScreen(f'Too slow')
                    core.wait(3)
                else:
                    #drawTextOnScreen(f'Your answer was : {answers[0]}')
                    #core.wait(1)
                    stop_eachq  = time.time()
                    print(f"You took {stop_eachq - start_eachq}s to answer")
                    # drawAnswer(corr_ans, answers[0])
                    #eegMarking(stop_eachq - start_eachq)
                    core.wait(3)

                drawFixation('task break', np.random.uniform(task_flixation_time[0], task_flixation_time[1]))

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
                    drawFixation('trial break', trial_flixation_time-wait)

                    #Perception
                    drawTrial(img-1, 'perception', stim_time)   # drawTrail(idx_mark, type_mark, stimTime)
                    drawFixation('task break', np.random.uniform(task_flixation_time[0], task_flixation_time[1]))
                    #Imagery
                    drawTrial(img-1, 'imagery', stim_time)

        drawTextOnScreen('End of experiment, Thank you')
        stop  = time.time()
        print(f"Total experiment time = {(stop-start)/60} ")
        core.wait(10)
        play = False

mywin.close()
core.quit()