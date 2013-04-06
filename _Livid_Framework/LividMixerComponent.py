import Live


from LividConstants import *
from LividChanStripComponent import LividChanStripComponent
from RGBButtonElement import RGBButtonElement
from Elementary import Elementary

from _Framework.MixerComponent import MixerComponent 
from _Framework.EncoderElement import EncoderElement 


class LividMixerComponent(MixerComponent, Elementary):
  def __init__(self, 
    sends = [], 
    mutes = [], 
    solos = [], 
    arms = [],
    selects = [], 
    master_select = None,
    crossfader = None, 
    master = None, 
    cue = None, 
    faders = [],
    **kwargs):

    MixerComponent.__init__(self, len(faders))
    Elementary.__init__(self, **kwargs)


    self.num_tracks = len(faders)
    self.name = "Mixer"
    self.set_track_offset(0)

    # One for each channel
    self.build_channel_strips(mutes, faders, sends, solos, arms, selects)

    # One-offs
    self.build_master(master, master_select)
    self.build_cue(cue)
    self.build_crossfader(crossfader)


  def build_channel_strips(self, mutes, faders, sends, solos, arms, selects):
    """ Go through each channel strip, assign all the relevant controls"""
    mute_buttons = self.extend([self.button(note) for note in mutes])
    fader_encoders = self.extend([self.encoder(cc) for cc in faders])
    solo_buttons = self.extend([self.button(note, on_color = PURPLE, off_color = BLUE) for note in solos])
    arm_buttons = self.extend([self.button(note, on_color = YELLOW, off_color = PURPLE) for note in arms])
    select_buttons = self.extend([self.button(note, on_color = GREEN, off_color = PURPLE) for note in selects])

    for i in range(self.num_tracks): # We've previously asserted that we have matching lengths of mutes etc
      strip = self.channel_strip(i)
      strip.set_invert_mute_feedback(True)
      strip.set_volume_control(fader_encoders[i])
      strip.set_mute_button(mute_buttons[i])
      strip.set_arm_button(arm_buttons[i])
      strip.set_solo_button(solo_buttons[i])
      strip.set_select_button(select_buttons[i])
      strip.set_send_controls(self.build_send_encoders(sends[i]))

  def build_master(self, master, select):
    """ Build and assign master volume fader if set """
    if master is not None:
      master_strip = self.master_strip()
      master_strip.set_volume_control(self.encoder(master))
      if select is not None:
        master_strip.set_select_button(self.button(select))

  def build_cue(self, cue):
    """ Build and assign the cue volume control if set """
    if cue is not None:
      self.set_prehear_volume_control(self.encoder(cue))

  def build_crossfader(self, crossfader):
    if crossfader is not None:
      self.set_crossfader_control(self.encoder(crossfader))
    
  def build_send_encoders(self, cc_list):
    """ Build a tuple of encoders from a list of CCs"""
    return tuple([self.encoder(cc) for cc in cc_list])
  
  # Treat returns as tracks
  #def tracks_to_use(self):
    #return (self.song().visible_tracks + self.song().return_tracks)

  def _create_strip(self):
    return LividChanStripComponent()

  def extend(self, list):
    list.extend([None] * (self.num_tracks - len(list)))
    return list

