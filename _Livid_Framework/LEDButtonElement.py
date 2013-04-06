from LividConstants import *
from Elementary import Elementary

from FlashingButtonElement import FlashingButtonElement
from RGBButtonElement import RGBButtonElement
from _Framework.ButtonElement import ButtonElement

class LEDButtonElement(RGBButtonElement):
  'Custom button element that can send state to multiple LEDs as needed'

  def __init__(self, 
      is_momentary,
      msg_type,
      channel,
      identifier,
      off_color = 0,
      on_color = 127,
      blink_on = False,
      blink_colors = [RED],
      color_mappings = None,
      **kwargs):

    RGBButtonElement.__init__(self, is_momentary, msg_type, channel, identifier, 
        blink_on = blink_on, 
        on_color = on_color,
        off_color = off_color,
        blink_colors = blink_colors)
    
    self.setup_color_mappings(color_mappings)

  def setup_color_mappings(self, color_mappings):
    self.leds = {}
    if color_mappings is not None:
      for value, note_offset in color_mappings.items():
        adjusted_identifier = self._msg_identifier + note_offset
        #if note_offset > 0: # Don't create an alias for the root button if it has one
        self.leds[value] = ButtonElement(True, self._msg_type, self._msg_channel, adjusted_identifier)

  def send_value(self, value, force_send=False):
    if value is 0:
      FlashingButtonElement.send_value(self, value, force_send)
    else:
      if self.leds.has_key(value):
        FlashingButtonElement.send_value(self, value, force_send)
        self.leds[value].send_value(127, True)
      else:
        FlashingButtonElement.send_value(self, value, force_send)

