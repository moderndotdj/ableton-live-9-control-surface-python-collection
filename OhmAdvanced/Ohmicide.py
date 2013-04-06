import Live

from Constants import *

from _Livid_Framework.LividMixerComponent import LividMixerComponent
from _Livid_Framework.LividSessionComponent import LividSessionComponent
from _Livid_Framework.LividTransportComponent import LividTransportComponent
from _Livid_Framework.LividSessionZoomingComponent import LividSessionZoomingComponent
from _Livid_Framework.LividControlSurface import LividControlSurface
from _Livid_Framework.LividBlinker import LividBlinker
from _Livid_Framework.LividVUMeter import LividVUMeter
from _Livid_Framework.MomentaryDeviceComponent import MomentaryDeviceComponent

class Ohmicide(LividControlSurface):
  __module__ = __name__
  __doc__ = " Ohmicide controller script "

  def __init__(self, c_instance):
    LividControlSurface.__init__(self, c_instance)
    # setup_mixer, setup_session and setup_transport are automatically run
    # Anything else must be run here

  def setup_custom(self):
    self.blinker = LividBlinker(LOGO)
    self.repeater = MomentaryDeviceComponent(name = "Repeats", buttons = REPEAT_BUTTONS)
    self.master_vu = LividVUMeter(MASTER_VU, parent = self)
  
  def setup_mixer(self):
    self.mixer = LividMixerComponent(faders = FADERS, sends = SENDS, 
        crossfader = CROSSFADER, 
        master = MASTER, 
        cue = CUE_VOLUME,
        solos = SOLOS,
        selects = TRACK_SELECTS, 
        master_select = MASTER_SELECT, 
        channel = CHANNEL)
        #mutes = MUTES)
  
  def setup_session(self):
    self.session = LividSessionComponent(matrix = MATRIX, 
        navigation = NAVIGATION_BUTTONS, 
        scene_launches = SCENE_LAUNCH, 
        stops = STOPS, 
        stop_all = STOP_ALL, 
        channel = CHANNEL,
        mixer = self.mixer)
    self.session_zoom = LividSessionZoomingComponent(session = self.session, shift = SHIFT, channel = CHANNEL)
    
    # Session zoom

  def setup_transport(self):
    self.transport = LividTransportComponent(play = PLAY, stop = STOP, 
        bpm_up = BPM_UP, bpm_down = BPM_DOWN, play_indicator = LIGHTS, 
        channel = CHANNEL)
    
