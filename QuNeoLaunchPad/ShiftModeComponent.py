import Live

from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from ConfigurableButtonElement import ConfigurableButtonElement
from MIDI_Map import *


class ShiftModeComponent(ModeSelectorComponent):
	__module__ = __name__
	__doc__ = ' Special Class that uses two shift buttons and is lockable '

	def __init__(self, script):
		ModeSelectorComponent.__init__(self)
		self._script = script
		self._mode_hold = None
		self.current_mode = 0
		self.shift_buttons = None
		
	def set_mode_hold(self, button):
		assert ((button == None) or isinstance(button, ButtonElement or ConfigurableButtonElement))
		if (self._mode_hold != None):
			self._mode_hold.remove_value_listener(self._shift_hold_value)
		self._mode_hold = button
		if (self._mode_hold != None):
			self._mode_hold.add_value_listener(self._shift_hold_value)
		self._script.request_rebuild_midi_map()
		
	def set_shift_mode_buttons(self):
		self.shift_buttons = []
		for index in range(6):
			self.shift_buttons.append(self._script.led_button(GRID_CHANNEL, TRACK_ARM[index], 127))
			if index == self.current_mode:
				self.shift_buttons[index].send_value (127, True)
			else:
				self.shift_buttons[index].send_value(40, True)
		self.set_mode_buttons(self.shift_buttons)
		
	def _shift_hold_value(self, value):
		if(value>0):
			self._script.shift_button.turn_on()
			self._script._disable_buttons()
			self.shift_buttons = None
			self.set_shift_mode_buttons()
		else:
			self._script.shift_button.turn_off()
			self.set_mode_buttons(None)
			self._mode(self.current_mode)
		
	def _mode(self, value):
		if (value == 0):
			self._script._update_grid()
			self._script.current_mode = 0
		elif(value == 1):
			self._script._mixer_mode()
			self._script.current_mode = 1
		elif(value == 2):
			self._script._volume_mode(0)
			self._script.current_mode = 2
		elif(value == 3):
			self._script._volume_mode(1)
			self._script.current_mode = 3
		elif(value == 4):
			self._script._volume_mode(2)
			self._script.current_mode = 4
		elif(value == 5):
			self._script._volume_mode(3)
			self._script.current_mode = 5
		elif(value == 6):
			self._script._step_sequencer()
			self._script.current_mode = 6
		else:
			None
			
	def set_mode_buttons(self, buttons):
		if (buttons != None):
			if (self.shift_buttons != buttons):
				self.shift_buttons.remove_value_listener(self._shift_buttons_value)
			self.shift_buttons = buttons
			if (self.shift_buttons != None):
				for button in self.shift_buttons:
					assert isinstance(button, ButtonElement)
					button.add_value_listener(self._shift_buttons_value, identify_sender=True)
		else:
			if (self.shift_buttons != None):
				for button in self.shift_buttons:
					button.remove_value_listener(self._shift_buttons_value)
			self.shift_buttons = None
			
	def _shift_buttons_value(self, value, sender):
		assert (self.shift_buttons != None)
		assert (value in range(128))
		mode = int(sender._note*0.5)
		self.current_mode = mode
		if value > 0:
			for i in range(6):
				if self.shift_buttons[i] != sender:
					self.shift_buttons[i].send_value(40)
				else:
					self.shift_buttons[i].send_value(127)
			