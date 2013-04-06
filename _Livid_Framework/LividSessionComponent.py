import Live

from LividConstants import *
from Elementary import Elementary

from _Framework.SessionComponent import SessionComponent
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ButtonElement import ButtonElement
from RGBButtonElement import RGBButtonElement

# Fuck yeah multiple inheritance
class LividSessionComponent(SessionComponent, Elementary):
  def __init__(self, matrix = [], 
      navigation = None, 
      scroll_navigation = None,
      scene_launches = [], 
      stops = [], 
      stop_all = None, 
      mixer = False,
      triggered_to_play_value = YELLOW,
      record_value = PURPLE,
      stopped_value = CYAN,
      started_value = GREEN,
      **kwargs):
    # We can infer the width and height from the button matrix
    SessionComponent.__init__(self, len(matrix[0]), len(matrix))
    Elementary.__init__(self, **kwargs)

    self.triggered_to_play_value = triggered_to_play_value
    self.record_value = record_value
    self.stopped_value = stopped_value
    self.started_value = started_value
    self.setup_matrix(matrix)
    self.setup_stops(stops, stop_all)

    if len(scene_launches) > 0:
      self.setup_scene_launch(scene_launches)

    self.setup_navigation(navigation, scroll_navigation)
    # Scene launch buttons next
   
    if mixer:
      self.set_mixer(mixer)


  def setup_stops(self, stops, stop_all):
    if len(stops) > 0:
      self.set_stop_track_clip_buttons(tuple([self.button(note, blink_on = True, blink_colors = [CYAN]) for note in stops]))
      self.set_stop_track_clip_value(CYAN)
    
    if stop_all:
      self.set_stop_all_clips_button(self.button(stop_all))

  def setup_scene_launch(self, scene_launches):
    self.scene_launch_buttons = [self.button(note, off_color = YELLOW) for note in scene_launches]
    
    for i, scene in enumerate(self._scenes):
      scene.set_launch_button(self.scene_launch_buttons[i])
      scene.set_triggered_value(PURPLE)

  def setup_navigation(self, navigation, scroll_navigation):
    if scroll_navigation is not None:
      self.scroll_vertical = self.encoder(scroll_navigation["vertical"], map_mode = Live.MidiMap.MapMode.relative_two_compliment)
      self.scroll_horizontal = self.encoder(scroll_navigation["horizontal"], map_mode = Live.MidiMap.MapMode.relative_two_compliment)
      self.scroll_vertical.add_value_listener(self.handle_scroll_vertical)
      self.scroll_horizontal.add_value_listener(self.handle_scroll_horizontal)

    if navigation is not None:
      self.up_button = self.button(navigation['up'], off_color = GREEN)    
      self.down_button = self.button(navigation['down'], off_color = GREEN)    
      self.left_button = self.button(navigation['left'], off_color = GREEN)    
      self.right_button = self.button(navigation['right'], off_color = GREEN)    
      self.set_scene_bank_buttons(self.down_button, self.up_button)
      self.set_track_bank_buttons(self.right_button, self.left_button)

  def setup_matrix(self, matrix):
    self.button_matrix = ButtonMatrixElement() 

    for scene_index, row in enumerate(matrix):
      scene = self.scene(scene_index)
      scene.name = 'Scene_' + str(scene_index)
      button_row = [self.button(cc, blink_on = True, off_color = OFF) for cc in row]
      for i, cc in enumerate(row):
        clip_slot = scene.clip_slot(i) 
        clip_slot.set_triggered_to_play_value(self.triggered_to_play_value)
        clip_slot.set_triggered_to_record_value(self.record_value)
        clip_slot.set_stopped_value(self.stopped_value)
        clip_slot.set_started_value(self.started_value)
        clip_slot.set_launch_button(button_row[i])

      self.button_matrix.add_row(tuple(button_row))

  def handle_scroll_vertical(self, value):
    if self.is_enabled():
      if value is 127:
        self.set_offsets(self._track_offset, max(0, self._scene_offset - 1))
      elif value is 1:
        self.set_offsets(self._track_offset, (self._scene_offset + 1))

  def handle_scroll_horizontal(self, value):
    if self.is_enabled():
      if value is 127:
        self.set_offsets(max(0, (self._track_offset - 1)), self._scene_offset)
      elif value is 1:
        self.set_offsets((self._track_offset + 1), self._scene_offset)

  def disconnect(self):
    self.scroll_vertical.remove_value_listener(self.handle_scroll_vertical)
    self.scroll_horizontal.remove_value_listener(self.handle_scroll_horizontal)
    SessionComponent.disconnect(self)

























