from LividConstants import *
from RGBButtonElement import RGBButtonElement
from Elementary import Elementary

from _Framework.SessionZoomingComponent import SessionZoomingComponent

class LividSessionZoomingComponent(SessionZoomingComponent, Elementary):
  """ Customized session zoom component with a real init function """

  def __init__(self, 
      session = None, 
      shift = None, 
      unselected_color = RED,
      selected_color = GREEN,
      **kwargs):

    Elementary.__init__(self, **kwargs)
    SessionZoomingComponent.__init__(self, session)
    
    self.set_button_matrix(session.button_matrix)
    self.set_zoom_button(self.button(shift, blink_on = True))

    self.set_stopped_value(unselected_color)
    self.set_selected_value(selected_color)

    self.set_nav_buttons(session.up_button, session.down_button, session.left_button, session.right_button)
    if hasattr(session, 'scene_launch_buttons'):
      self.set_scene_bank_buttons(tuple(session.scene_launch_buttons))
