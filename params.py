from tools import sound_freq_sweep,compound_sound
import numpy as np
from psychopy.sound import Sound
from psychopy import visual

p = dict(
    # Display:
    monitor = 'CRT_NEC_FE992',
    full_screen = True,
    screen_number = 1,
    # Sounds:
    correct_sound = Sound(sound_freq_sweep(1000,2500,.1)),
    incorrect_sound = Sound(sound_freq_sweep(8000, 100, .1)),
    # General:
    n_trials = 150,
    fixation_size = 0.1,
    rgb = np.array([1.,1.,1.]),
    # Element array:
    sf = 4,
    elems_per_row = 30,
    elem_size = 2.5,
    elem_spacing = 1,
    jitter = 0.08,
    res = 128,
    # Cue:
    cue_size = [2,2],
    line_width = 5,
    # Timing: 
    cue_dur = 0.2,
    cue_to_ea = 0.6,
    #texture_dur =  0.05,
    mask_dur =  0.2,
    middle_fix_dur = 0.5,
    iti = .2
    )
