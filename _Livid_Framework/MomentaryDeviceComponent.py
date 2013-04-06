import Live

from LividConstants import *

from Elementary import Elementary
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class MomentaryDeviceComponent(ControlSurfaceComponent, Elementary):
  """ Will bind to device on specified channel with provided name, provide momentary control """

  def __init__(self, 
      track = "master", 
      name = None, 
      buttons = [], 
      on_color = PURPLE, 
      off_color = WHITE, 
      **kwargs):
    ControlSurfaceComponent.__init__(self)
    Elementary.__init__(self, **kwargs)
    self.on_color = on_color
    self.off_color = off_color

    if track == "master":
      self.track = self.song().master_track
    if name == None:
      self.device = self.track.devices[-1]
    else:
      for device in self.track.devices:
        if device.name == name:
          self.device = device
    self.setup_controls(buttons)

  def setup_controls(self, buttons):
    self.buttons = [self.button(note, on_color = self.on_color, off_color = self.off_color) for note in buttons]
    for i, button in enumerate(self.buttons):
      button.index = i
      button.add_value_listener(self.device_toggle, True)
      button.turn_off()

  def device_toggle(self, value, sender):
    # 1 + index because first parameter is on/off
    if value > 0:
      self.device.parameters[1 + sender.index].value = 127
    else:
      self.device.parameters[1 + sender.index].value = 0
    if value > 0:
      sender.send_value(sender.on_color)
    else:
      sender.send_value(sender.off_color)


  def update(self):
    for button in self.buttons:
      button.turn_off()
    return None

  def disconnect(self):
    for button in self.buttons:
      button.remove_value_listener(self.device_toggle)
