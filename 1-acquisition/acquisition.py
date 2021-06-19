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

operators= {
    '+': operator.add, 
    '-': operator.sub,
    'x': operator.mul,
    '/': operator.truediv,
}

def drawStress(level):
    operant1 = random.randint(0,9)
    operant2 = random.randint(1,9)
    operator1 = random.choice(list(operators.keys()))
    #operator2 = random.choice(operators.keys())

    if level == "low":
        ans = operators[operator1](operant1, operant2)
        if type(ans) == int and operator == "+" or "-" and 0 <= ans <=9:
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2}', languageStyle='LTR')
            message.contrast =  0.3
            message.height= 0.5
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw      
        else:
            drawStress(level) 

    if level == "mild" or "higher":
        ans = operators[operator1](operant1, operant2)
        if type(ans) == int and 0 <= ans <=9:
            message = visual.TextStim( mywin, text=f'{operant1} {operator1} {operant2}', languageStyle='LTR')
            message.contrast =  0.3
            message.height= 0.5
            message.draw() # draw on screen
            mywin.flip()   # refresh to show what we have draw      
        else:
            drawStress(level)    

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
#     if not(isTrianing) and fileName == 'trial break':
#         text = f"Block {block+1} / {num_block}"
#         message = visual.TextStim( mywin, text=text, languageStyle='LTR' )
#         message.contrast =  0.3
#         message.pos = (0, -0.6)
#         message.draw() # draw on screen
        
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


trial_idx = input()

wait = 1
    
# mywin = visual.Window([1366, 768], color='black', fullscr=True, screen=1, units='norm')     # set the screen and full screen mode
# mywin = visual.Window([640, 360], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode
mywin = visual.Window([1366, 768], color='black', fullscr=False, screen=0, units='norm')     # set the screen and full screen mode

drawTextOnScreen('Loading...')

#Load stimuli to RAM
#rng = default_rng()
#fname = rng.choice(5, size=3, replace=False)
#fname = fname.astype(str).tolist()
#usefilefname = fname
#usefilefname.append('black')

#all_imgs = []
#for image_folder in image_folders:
#    all_img = []
#    for im in usefilefname:
#        imgPath=image_folder+"/"+str(im)+".png"
#        stim = visual.ImageStim( mywin,  image=imgPath )
#    #     stim.size *= .7
#        if im == 'black':
#            blank = stim
#        else:
#            all_img.append(stim)
#    all_imgs.append(all_img)

core.wait(3)
        
##############
####  Training session
while True:
    isTrianing = True
    drawTextOnScreen('Training session\nPlease wait\nPress space bar to start')
    keys = event.getKeys()
    if 'space' in keys:      # If space has been pushed
        start = time.time()
        drawTextOnScreen('') 

        for i,level in enumerate(levels):
            drawTextOnScreen(f'Examples of {levels[i]}')
            core.wait(wait)
            for img in range(10):
                drawStress(level)
                #drawTextOnScreen(f'Trial {trial}/5')
                core.wait(wait)
                clear_output(wait=True)
                drawFixation('trial break', trial_flixation_time-wait)
                
                #Perception
                #drawTrial(int(img)-1, 'perception', stim_time)   # drawTrail(idx_mark, type_mark, stimTime)
                drawTextOnScreen(f'ANSWER')
                core.wait(wait)
                drawFixation('task break', np.random.uniform(task_flixation_time[0], task_flixation_time[1]))
                #Imagery
                #drawTrial(int(img)-1, 'imagery', stim_time)

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