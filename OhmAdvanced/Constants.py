from _Livid_Framework.LividConstants import *

MIDI_CC_TYPE = 1
MIDI_NOTE_TYPE = 0

RETURNS = 0
CHANNEL = 0 # All things must be on one channel

# Transport
PLAY = {"note" : 69, "on_color" : PURPLE, "off_color" : WHITE, "blink_on" : True, "blink_colors" : [PURPLE, BLUE]}
STOP = 71
SHIFT = 87

BPM_UP = 72
BPM_DOWN = 64

LOGO = 119
LIGHTS = 118

# It is assumed that these will use the global channel
# And will be CCs
FADERS = [23, 22, 15, 14, 5, 7, 6, 4] 
MASTER = None
CROSSFADER = 24 

# Each channel is a tuple of send encoders from bottom to top
SENDS = [
  [21, 19, 17], # Channel 1
  [20, 18, 16], # Channel 2 etc
  [13, 11, 9],
  [12, 10, 8],
  [3],
  [1],
  [0],
  [2]]
CUE_VOLUME = 2

NAVIGATION_BUTTONS = {
    'up' : 70,
    'down' : 78,
    'left' : 77,
    'right' : 79}
# Grid of button notes
MATRIX = [
    [0, 8,  16, 24, 32, 40, 48, 56],
    [1, 9,  17, 25, 33, 41, 49, 57],
    [2, 10, 18, 26, 34, 42, 50, 58],
    [3, 11, 19, 27, 35, 43, 51, 59],
    [4, 12, 20, 28, 36, 44, 52, 60]]

#SCENE_LAUNCH = [56, 57, 58, 59, 60]
SCENE_LAUNCH = []

STOPS = [5, 13, 21, 29, 37, 45, 53, 61]
STOP_ALL = None

SOLOS = [6, 14, 22, 30]# 38, 46, 54, 62]

MASTER_VU =  [7, 15, 23, 31, 39, 47, 55, 63]

#TRACK_SELECTS =  [65, 73, 66, 74, 67, 75, 68, 76]
TRACK_SELECTS =  [65, 73, 66, 74]
MASTER_SELECT = None

REPEAT_BUTTONS = [
    {"note" : 67, "on_color" : PURPLE, "off_color" : WHITE},
    {"note" : 75, "on_color" : GREEN, "off_color" : CYAN},
    {"note" : 68, "on_color" : PURPLE, "off_color" : WHITE},
    {"note" : 76, "on_color" : GREEN, "off_color" : CYAN}]


