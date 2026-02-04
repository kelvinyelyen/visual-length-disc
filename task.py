"""
THE INSTRUMENT
Goal: Measure the internal noise in your visual cortex.
Method: Constant Stimuli (randomized fixed levels).
"""
from psychopy import visual, core, event
import pandas as pd
import random

# --- 1. THE PHYSICS (Parameters) ---
# We anchor reality to a standard line of 200 pixels.
STANDARD_PX = 200 

# We test these specific deviations from reality.
# 0.9 = 10% shorter, 1.1 = 10% longer.
RATIOS = [0.90, 0.95, 0.98, 1.0, 1.02, 1.05, 1.10]
TRIALS_PER_LEVEL = 10  # 7 levels * 10 reps = 70 total trials

# --- 2. THE SETUP ---
win = visual.Window([1000, 600], color=[-1,-1,-1], units='pix') # Dark mode

# The "Standard" and "Test" lines (placeholders)
line_L = visual.Line(win, start=(-150,0), end=(-50,0), lineWidth=5, lineColor='white')
line_R = visual.Line(win, start=(50,0),  end=(150,0), lineWidth=5, lineColor='white')
fixation = visual.TextStim(win, text='+', color='grey')

# Generate the trial list (The "Design Matrix")
trials = []
for r in RATIOS:
    for i in range(TRIALS_PER_LEVEL):
        # We randomize side to ensure we aren't measuring a "left-side bias"
        trials.append({'ratio': r, 'std_side': random.choice(['left', 'right'])})
random.shuffle(trials) 

# --- 3. THE LOOP ---
data = []

# Instruction
visual.TextStim(win, text="F = Left is Longer\nJ = Right is Longer\n\nSpace to start").draw()
win.flip()
event.waitKeys(keyList=['space'])

for t in trials:
    # A. Define the physical reality for this trial
    std_len = STANDARD_PX
    test_len = STANDARD_PX * t['ratio']
    
    # Assign lengths to Left/Right based on randomization
    if t['std_side'] == 'left':
        len_L, len_R = std_len, test_len
    else:
        len_L, len_R = test_len, std_len
        
    # Update line geometry (centering them)
    line_L.start, line_L.end = (-250 - len_L/2, 0), (-250 + len_L/2, 0)
    line_R.start, line_R.end = ( 250 - len_R/2, 0), ( 250 + len_R/2, 0)

    # B. Fixation (Reset the eyes)
    fixation.draw()
    win.flip()
    core.wait(0.5)

    # C. Stimulus (The Event)
    line_L.draw()
    line_R.draw()
    win.flip()
    core.wait(0.4) # Flash for 400ms
    win.flip()     # Blank screen

    # D. Response (The Measurement)
    keys = event.waitKeys(keyList=['f', 'j'])
    resp = keys[0]
    
    # E. Logic: Did you think the TEST (variable) line was longer?
    # This is the standard way to code 2AFC data.
    # 1 = "I perceive the Test as longer"
    # 0 = "I perceive the Standard as longer"
    
    perceived_test_longer = 0
    # If Test was on Right (std=left) AND user pressed J (right) -> 1
    if t['std_side'] == 'left' and resp == 'j': perceived_test_longer = 1
    # If Test was on Left (std=right) AND user pressed F (left) -> 1
    if t['std_side'] == 'right' and resp == 'f': perceived_test_longer = 1
    
    data.append({
        'ratio': t['ratio'], 
        'response': perceived_test_longer
    })

# --- 4. OUTPUT ---
pd.DataFrame(data).to_csv('my_psychophysics_data.csv', index=False)
win.close()
print("Session Complete. Data saved.")