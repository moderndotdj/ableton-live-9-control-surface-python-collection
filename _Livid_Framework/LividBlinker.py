import Live

from RGBButtonElement import RGBButtonElement
from Elementary import Elementary
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class LividBlinker(ControlSurfaceComponent, Elementary):
  """ Control surface component that will init and blink an LED on a timer"""

  def __init__(self, led = None, **kwargs):
    ControlSurfaceComponent.__init__(self)
    Elementary.__init__(self, **kwargs)

    if led:
      self.setup_blinker(led)

  def setup_blinker(self, led):
    self.led = self.encoder(led)
    self.song().add_current_song_time_listener(self.blink)
    self.on = True
    self.counter = 0
    self.led.send_value(127)
    self._show_msg_callback("LOADED")
    self.prev_position = 0
    self.on = False



  # Catch play/pause and reset


  def blink(self):
    position = int(self.song().current_song_time)
    if int(position) != int(self.prev_position):
      self.prev_position = position
      if self.on: 
        self.led.send_value(0, True)
        self.on = False
      else:
        self.led.send_value(127, True)
        self.on = True

  def update(self):

    return None

  def disconnect(self):
    self.song().remove_current_song_time_listener(self.blink)
    return None

