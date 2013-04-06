TRACK_OFFSET = -1 #offset from the left of linked session origin; set to -1 for auto-joining of multiple instances
SCENE_OFFSET = 0

# MIDI CHANNEL NUMBERS
PAD_CHANNEL = 8
GRID_CHANNEL = 2
NOTE_OFFSET = 9
DRUM_RACK_CHANNEL = 5
METRO_CHANNEL = 5

# LED COLORS
RED_HI = 127
RED_LO = 110
GREEN_HI = 40
GREEN_LO = 10
ORANGE_HI = 80
ORANGE_LO = 60

ZERO_DB = 0.0

# SHIFT BUTTON
SHIFT_BUTTON = 45

# TRANSPORT CONTROLS
PLAY = 35
STOP = 34
REC = 33
TAP_TEMPO = 36
LOOP = 39
OVERDUB = 39
METRONOME = 38

TEMPO_UP = 37
TEMPO_DOWN = 36

SEND_A = 6
SEND_B = 7

# Device Control
DEVICELOCK = -1 #Device Lock (lock "blue hand")
DEVICEONOFF = -1 #Device on/off
DEVICENAVLEFT = -1 #Device nav left
DEVICENAVRIGHT = -1 #Device nav right
DEVICEBANKNAVLEFT = -1 #Device bank nav left
DEVICEBANKNAVRIGHT = -1 #Device bank nav right
DEVICEBANK = (-1, #Bank 1 #All 8 banks must be assigned to positive values in order for bank selection to work
              -1, #Bank 2 
              -1, #Bank 3 
              -1, #Bank 4 
              -1, #Bank 5 
              -1, #Bank 6
              -1, #Bank 7
              -1, #Bank 8
              )

# Arrangement View Controls
SEEKFWD = -1 #Seek forward
SEEKRWD = -1 #Seek rewind

# Session Navigation (aka "red box")
SESSION_LEFT = 42 #Session left
SESSION_RIGHT = 43 #Session right
SESSION_UP = 47 #Session up
SESSION_DOWN = 46 #Session down

# Track Navigation
TRACK_LEFT = 40 #Track left
TRACK_RIGHT = 41 #Track right

# Scene Navigation
SCENE_UP = 48 #Scene down
SCENE_DOWN = 49 #Scene up

# Scene Launch
SLOT_LAUNCH = 14 #Selected scene launch

SCENE_LAUNCH = [126,
                110,
                94,
                78,
                62,
                46,
                30]
                
# SCENE_LAUNCH = [99, 95, 91, 87, 83, 79, 75, 71]

MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11, 12]
MAJOR_SCALE.reverse()

CHROMATIC_SCALE = [0, 1, 2, 3, 4, 5, 6, 7]
CHROMATIC_SCALE.reverse()

# STOP_TRACK =   [  0,   2,  4,  6,  8, 10, 12] #STOP TRACK with 7x7 Tracks
# STOP_TRACK_2 = [ 48,  50, 52, 54, 56, 58, 60] #STOP TRACK with 4x7 Tracks

# LED_METRO = [48, 50, 52, 54, 56, 58, 60, 62] #LED METRONOME BUTTONS
# LED_METRO_2 = [49, 53, 57, 61] #LED METRONOME BUTTONS
# LED_METRO_2 = [49, 51, 53, 55, 57, 59, 61, 63] #LED METRONOME BUTTONS

# Clip Launch / Stop
# STOP_ALL_CLIPS = 14 #Stop all clips
STOP_ALL_CLIPS = 62

# 7x7 Matrix NOTE ASSIGNMENT
CLIP_NOTE_MAP = [[112, 114, 116, 118, 120, 122, 124, 126],
                 [ 96,  98, 100, 102, 104, 106, 108, 110],
                 [ 80,  82,  84,  86,  88,  90,  92,  94],
                 [ 64,  66,  68,  70,  72,  74,  76,  78],
                 [ 48,  50,  52,  54,  56,  58,  60,  62],
                 [ 32,  34,  36,  38,  40,  42,  44,  46],
                 [ 16,  18,  20,  22,  24,  26,  28,  30],
                 [  0,   2,   4,   6,   8,  10,  12,  14]]

# CLIP_NOTE_MAP = [[64, 65, 66, 67, 96, 97, 98, 99],
#                  [60, 61, 62, 63, 92, 93, 94, 95],
#                  [56, 57, 58, 59, 88, 89, 90, 91],
#                  [52, 53, 54, 55, 84, 85, 86, 87],
#                  [48, 49, 50, 51, 80, 81, 82, 83],
#                  [44, 45, 46, 47, 76, 77, 78, 79],
#                  [40, 41, 42, 43, 72, 73, 74, 75],
#                  [36, 37, 38, 39, 68, 69, 70, 71]]

STEP_SEQUENCER_MAP = CLIP_NOTE_MAP

# Track Control
MASTERSEL = -1 #Master track select

TRACK_MUTE = [32, 34, 36, 38, 40, 42, 44, 46]
TRACK_SOLO = [16, 18, 20, 22, 24, 26, 28, 30]
TRACK_ARM =  [ 0,  2,  4,  6,  8, 10, 12, 14]

STOP_TRACK = [ 48, 50, 52, 54, 56, 58, 60]
# TRACK_MUTE = [44, 45, 46, 47, 76, 77, 78, 79]
# TRACK_SOLO = [40, 41, 42, 43, 72, 73, 74, 75]
# TRACK_ARM = [36, 37, 38, 39, 68, 69, 70, 71]

# Pad Translations for Drum Rack
DRUM_PADS = [[12, 13, 14, 15],
             [ 8,  9, 10, 11],
             [ 4,  5,  6,  7],
             [ 0,  1,  2,  3]]

DRUM_RACK_UP = 46
DRUM_RACK_DOWN = 47

SLIDER_CHANNEL = 8 #Channel assignment for all mapped CCs; valid range is 0 to 15
TEMPO_TOP = 140.0 # Upper limit of tempo control in BPM (max is 999)
TEMPO_BOTTOM = 40.0 # Lower limit of tempo control in BPM (min is 0)

TEMPO_CONTROL = 11 #Tempo control CC assignment; control range is set above
TEMPO_FINE = 10 #Tempo control CC assignment; control range is set above

MASTERVOLUME = -1 #Master track volume
CUELEVEL = -1 #Cue level control
CROSSFADER = 5 #Crossfader control

SELECTED_SENDS = [11, 10]
SELECTED_PAN = 9
SELECTED_VOL = 8
TRACK_VOL = [1, 2, 3, 4]
