import Live
from LividConstants import *
from Elementary import Elementary
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent

class LividVUMeter(ControlSurfaceComponent, Elementary):
  """ An abstraction for a VU meter using a single MIDI CC"""

  def __init__(self, target, led_range = [0.52, 0.92], track = "master", parent = None, **kwargs):
    ControlSurfaceComponent.__init__(self)
    Elementary.__init__(self, **kwargs)
    
    self.parent = parent
    self.bottom = led_range[0] 
    self.top = led_range[1] 
    self.calculate_multiplier(target)
    if target:
      self.setup_vu(target)


  def setup_vu(self, target):
    if isinstance(target, list):
      self.leds = [self.button(note) for note in target]
      self.render = self.render_leds
    else:
      self.target = self.encoder(target)
      self.render = self.render_encoder
    self.track = self.song().master_track
    self.prev_value = 0
    self.track.add_output_meter_left_listener(self.observe)

  def observe(self):
    scaled_value = self.level()
    if scaled_value is not self.prev_value:
      self.prev_value = scaled_value
      self.render(scaled_value)

  def render_encoder(int_value):
    self.target.send_value(int_value, True)

  def render_leds(self, int_value):
    for i, led in enumerate(self.leds):
      if (i + 1) <= int_value:
        if i is 5 or i is 6:
          led.send_value(YELLOW, True)
        elif i > 6:
          led.send_value(RED, True)
        else:
          led.send_value(GREEN, True)
      else:
        led.send_value(0, True)


  def level(self):
    return self.scale(self.track.output_meter_left)

  def scale(self, value):
    if (value > self.top):
      value = self.top
    elif (value < self.bottom):
      value = self.bottom

    value = value - self.bottom
    value = value * self.multiplier 
    value =  int(round(value))
    return value

  def calculate_multiplier(self, target):
    if isinstance(target, list):
      self.multiplier = (len(target) / (self.top - self.bottom))
    else:
      self.multiplier = (127 / (self.top - self.bottom))
  
  def update(self):
    return None
  
  def disconnect(self):
    self.track.remove_output_meter_left_listener(self.observe)


