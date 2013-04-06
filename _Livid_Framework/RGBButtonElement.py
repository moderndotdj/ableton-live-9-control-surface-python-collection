from FlashingButtonElement import FlashingButtonElement
from _Framework.ButtonElement import ButtonElement
from LividConstants import *

class RGBButtonElement(FlashingButtonElement):
  'Modified ButtonElement with configurable off and on states'

  def __init__(self, is_momentary, 
      msg_type, 
      channel, 
      identifier, 
      on_color = GREEN,
      off_color = RED, 
      blink_on = False,
      blink_colors = [YELLOW]):

    FlashingButtonElement.__init__(self, is_momentary, msg_type, channel, identifier, 
        blink_on = blink_on, 
        blink_colors = blink_colors)

    self.on_color = on_color
    self.off_color = off_color

  def turn_on(self):
    self.send_value(self.on_color)

  def turn_off(self):
    self.send_value(self.off_color)

