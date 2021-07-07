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
# Get experiment parameters
#==============================================
par = input('Participant : ')

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

color = {'Red   ':(255, 0, 0),
        'Green ':(0, 255, 0),
        'Blue  ':(0, 0, 255),
        'Purple' : (148,0,211),
        'Orange': (255,165,0),
        'Yellow' :(255,255,0),
        }
word = ['Red   ', 'Green ', 'Blue  ', 'Purple', 'Orange', 'Yellow']

def get_corr_ans(color, search_code):
    for color_name, code in color.items():
        if code == search_code:
            return color_name

def get_choices(level,all_words,corr_ans,num):

    if level == 'LowStress':
        choices = []
        choice1 = random.sample(all_words, num)
        choice2 = random.sample(all_words, num)
        choice3 = random.sample(all_words, num)
        choices.append(choice1)
        choices.append(choice2)
        choices.append(choice3)
        choices.append(all_words)

    else :
        choices = []
        choice1 = random.sample(corr_ans, num)
        choice2 = random.sample(all_words, num)
        choices.append(choice1)
        choices.append(choice2)
        choices.append(all_words)
        choices.append(corr_ans)

    choices = random.sample(choices, len(choices))
    choice_check = [i for n, i in enumerate(choices) if i not in choices[:n]]

    idx_ans = choices.index(corr_ans)

    if len(choice_check) < 4:
        # print("yes=================================================================")
        return get_choices(level,all_words,corr_ans,num)
    else :
        return choices, idx_ans
    
def drawStroop(level):
    if level == "LowStress":
        idxs = np.random.choice(6, 3, replace=False)
        all_words = [word[i] for i in idxs]
        all_colors = [color[all_words[j]] for j in range(3)]
        corr_ans = [get_corr_ans(color, all_colors[i]) for i in range(3)]
        all_position = [(-0.5, 0.6), (0, 0.6), (0.5, 0.6)]

        
        for i in range(len(all_words)):
            message = visual.TextStim( mywin, text=f'{all_words[i]}\t', languageStyle='LTR',bold=True)
            message.contrast =  0.3
            message.height = 0.2
            message.colorSpace = 'rgb255'
            message.color = all_colors[i]
            message.pos = all_position[i]
            message.draw() # draw on screen

        choices, idx_ans = get_choices(level,all_words,corr_ans,3)
        textbox = visual.TextBox(
                    window=mywin,
                    text=f'1) {choices[0][0]} {choices[0][1]} {choices[0][2]}\n2) {choices[1][0]} {choices[1][1]} {choices[1][2]}\n3) {choices[2][0]} {choices[2][1]} {choices[2][2]}\n4) {choices[3][0]} {choices[3][1]} {choices[3][2]}',
                    font_size=60,
                    # font_name=None,# only mono space fonts are supported
                    font_color=[1,1,1],
                    background_color=[-1,-1,-1], # fill the stim background
                    textgrid_shape=[24,4],  # specify area of text box
                    pos=(0,-0.15),
                    grid_horz_justification='left',
                    grid_vert_justification='center')
        textbox.draw()

        mywin.flip()
        eegMarking('stroop', level, 'start')   # refresh to show what we have draw
        return idx_ans + 1
              

    elif level == "MildStress":

        idx_word = np.random.choice(6, 3, replace=False)
        idx_color = np.random.choice(6, 3, replace=False)
        
        all_words = [word[i] for i in idx_word]
        all_colors = [color[word[j]] for j in idx_color]
        corr_ans = [get_corr_ans(color, all_colors[i]) for i in range(3)]
        all_position = [(-0.5, 0.6), (0, 0.6),(0.5, 0.6)]
        
        if (idx_word[0] != idx_color[0])and (idx_word[1] != idx_color[1]) and (idx_word[2] != idx_color[2]):
            
            for i in range(len(all_words)):
                message = visual.TextStim( mywin, text=f'{all_words[i]}\t', languageStyle='LTR',bold=True)
                message.contrast =  0.3
                message.height = 0.2
                message.colorSpace = 'rgb255'
                message.color = all_colors[i]
                message.pos = all_position[i]
                message.draw() # draw on screen
            
            choices, idx_ans = get_choices(level,all_words,corr_ans,3)

            textbox = visual.TextBox(
                    window=mywin,
                    text=f'1) {choices[0][0]} {choices[0][1]} {choices[0][2]}\n2) {choices[1][0]} {choices[1][1]} {choices[1][2]}\n3) {choices[2][0]} {choices[2][1]} {choices[2][2]}\n4) {choices[3][0]} {choices[3][1]} {choices[3][2]}',
                    font_size=60,
                    # font_name=None,# only mono space fonts are supported
                    font_color=[1,1,1],
                    background_color=[-1,-1,-1], # fill the stim background
                    textgrid_shape=[24,4],  # specify area of text box
                    pos=(0,-0.15),
                    grid_horz_justification='left',
                    grid_vert_justification='center')
            textbox.draw()

            mywin.flip()   # refresh to show what we have draw
            eegMarking('stroop', level, 'start')
            return idx_ans + 1
        else: 
            return drawStroop(level)
 
    else :
        idx_word = np.random.choice(6, 4, replace=False)
        idx_color = np.random.choice(6, 4, replace=False)
        
        all_words = [word[i] for i in idx_word]
        all_colors = [color[word[j]] for j in idx_color]
        corr_ans = [get_corr_ans(color, all_colors[i]) for i in range(4)]

        all_position = [(-0.6, 0.6), (-0.2, 0.6), (0.2, 0.6), (0.6, 0.6)]
        

        if (idx_word[0] != idx_color[0])and (idx_word[1] != idx_color[1]) and (idx_word[2] != idx_color[2]) and (idx_word[3] != idx_color[3]):
            for i in range(len(all_words)):
                message = visual.TextStim( mywin, text=f'{all_words[i]}\t', languageStyle='LTR',bold=True)
                message.contrast =  0.3
                message.height = 0.2
                message.colorSpace = 'rgb255'
                message.color = all_colors[i]
                message.pos = all_position[i]
                message.draw() # draw on screen
            
            choices, idx_ans = get_choices(level,all_words,corr_ans, 4)
            textbox = visual.TextBox(
                    window=mywin,
                    text=f'1) {choices[0][0]} {choices[0][1]} {choices[0][2]} {choices[0][3]}\n2) {choices[1][0]} {choices[1][1]} {choices[1][2]} {choices[1][3]}\n3) {choices[2][0]} {choices[2][1]} {choices[2][2]} {choices[2][3]}\n4) {choices[3][0]} {choices[3][1]} {choices[3][2]} {choices[3][3]}',
                    font_size=50,
                    # font_name=None,# only mono space fonts are supported
                    font_color=[1,1,1],
                    background_color=[-1,-1,-1], # fill the stim background
                    textgrid_shape=[32,4],  # specify area of text box
                    pos=(0,-0.15),
                    grid_horz_justification='left',
                    grid_vert_justification='center')
            textbox.draw()
            mywin.flip()   # refresh to show what we have draw
            eegMarking('stroop', level, 'start')
            return idx_ans + 1
        else: 
            return drawStroop(level)

def drawAnswer(corr_ans, ans):
    print(ans[-1])
    if (ans!='num_1') and (ans!='num_2') and (ans!='num_3') and (ans!='num_4'): 
        marking = "O"
        message_ = "An integer between 1-4 is required."
        message = visual.TextStim( mywin, text=message_, languageStyle='LTR')
        message.contrast =  0.3
        message.height= 0.07
        message.draw() # draw on screen
        mywin.flip()   # refresh to show what we have draw
        core.wait(0.5)

    elif corr_ans == int(ans[-1]):
        # message_ = "Correct!"
        marking = "T"
        # print(message_)
    else:
        # message_ = "Incorrect!"
        marking = "F"
        # print(message_)
    eegMarking('stroop', level, marking)
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
     
###############################  Control Phase ##################################
# to calculate avg time taken to answer for each stress level

avg_times = {level: [] for level in levels}

while True:
    drawTextOnScreen('Control Session\nPlease wait\nPress ENTER to start')
    keys = event.getKeys()
    if 'num_enter' in keys: # If spacebar has been pressed
        print("="*51)
        print(f"======= PAR {par} | START STROOP CONTROL SESSION =======")
        print("="*51)
        drawTextOnScreen('') 
        for idx,level in enumerate(levels): # for each level
            drawTextOnScreen(f'Level {idx+1}')
            core.wait(1)
            block_ = 0
            while block_ < num_block: # 4 blocks
                drawTextOnScreen(f'Block {block_ + 1}/4')
                core.wait(1)
                timeout_start = time.time()
                while time.time() < timeout_start + block_time: # block_time = 50
                    start_eachq = time.time()
                    corr_ans = drawStroop(level) # Draw Stroop & make eegMarker and get the correct answer

                    # # for draw stroop
                    # try:
                    #     os.makedirs('Stroop')
                    # except:
                    #     pass
                    # filename = f"Stroop/par{par}_stroop_control_markers.csv"
                    # mode = 'a' if os.path.exists(filename) else 'w'
                    # with open(f"Stroop/par{par}_stroop_control_markers.csv", mode) as myfile:
                    #     fileEmpty = os.stat(filename).st_size == 0
                    #     headers = ['Time', 'Task', 'Level' , 'Marking']
                    #     writer = csv.DictWriter(myfile, delimiter=',', lineterminator='\n', fieldnames=headers)
                    #     if fileEmpty:
                    #         writer.writeheader()  # file doesn't exist yet, write a header
                    #     writer.writerow({'Time': time.time(), 'Task': 'stroop', 'Level': level, 'Marking': 'start'})

                    answers = event.waitKeys() # wait until we get the answer
                    marking = drawAnswer(corr_ans, answers[0]) # check the answer & make eegMarker
                    print(f"User's answer: {answers}")
                    
                    # time the answer and get the average answer time
                    stop_eachq  = time.time()
                    ans_time = stop_eachq - start_eachq
                    avg_times[level].append(ans_time)
                    print(f"Answer time: {ans_time}")
                    print("="*10)

                block_ += 1
                drawFixation(block_break) # block_break = 20 & eegMarking
        
            # time for questionaire at the end of the level
            if idx == 0: # at the end of the first level do both pairwise and the questionaire
                drawTextOnScreen('Pairwise & Questionnaire')
                core.wait(90)
                drawTextOnScreen('Please prepare for next level')
                core.wait(1)
            elif idx == 2: # at the end of the first level do both pairwise and the questionaire
                drawTextOnScreen('Questionnaire')
                core.wait(60)
            else :
                drawTextOnScreen('Questionnaire')
                core.wait(60)
                drawTextOnScreen('Please prepare for next level')
                core.wait(3)
            
        avg_low = statistics.mean(avg_times['LowStress']) * 0.9
        avg_mild = statistics.mean(avg_times['MildStress']) * 0.9
        avg_higher = statistics.mean(avg_times['HigherStress']) * 0.9

        # Save the average answering time for each level to csv
        try:
            os.makedirs('Stroop')
        except:
            pass
        filename = f"Stroop/stroop_control_time.csv"
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(f"Stroop/stroop_control_time.csv", mode) as myfile:
            fileEmpty = os.stat(filename).st_size == 0
            headers = ['Participant', 'LowStress' , 'MildStress', 'HigherStress']
            writer = csv.DictWriter(myfile, delimiter=',', lineterminator='\n',fieldnames=headers)
            if fileEmpty:
                writer.writeheader()  # file doesn't exist yet, write a header
            writer.writerow({'Participant': par, 'LowStress': avg_low, 'MildStress': avg_mild, 'HigherStress': avg_higher})
        print("*** AVERAGE TIME SAVED ! *** ")

        drawTextOnScreen('End of Control Session\nPress ENTER to end')
        _ = event.waitKeys()
        break

mywin.close()
core.quit()
print("="*51)
print(f"======= PAR {par} | STROOP CONTROL SESSION ENDED =======")
print("="*51)
