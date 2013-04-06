# emacs-mode: -*- python-*-
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from OhmButton import OhmButton

class PageModeComponent(ModeSelectorComponent):
	__module__ = __name__
	__doc__ = ' Special Class that uses bank buttons to switch between pages '

	def __init__(self, script):
		ModeSelectorComponent.__init__(self)
		self._script = script
		self._mode_toggle = [None,None,None,None,None,None]
		self._mode_index = 0
		self._shift = False

	def set_mode_toggle(self, menu):
		for index in range(6):
			if (self._mode_toggle[index] != None):
				self._mode_toggle[index].remove_value_listener(self._toggle_value)
			self._mode_toggle[index] = menu[index]
			if (self._mode_toggle[index] != None):
				self._mode_toggle[index].add_value_listener(self._toggle_value,True)
		
		self._script.request_rebuild_midi_map()

		
	def _toggle_value(self, value, sender):
		assert isinstance(value, int)
		if value > 0:
			self.set_mode(sender.menu_nr)
		
	def number_of_modes(self):
		return 12

	def set_mode(self, mode):
		assert isinstance(mode, int)
		assert (mode in range(self.number_of_modes()))
		if self._shift:
			mode = mode + 6
		if (self._mode_index != mode):
			self._mode_index = mode
			self.update()



	def update(self):
		for index in range(6):
			self._mode_toggle[index].turn_off()
		if self._mode_index > 5:
			self._mode_toggle[self._mode_index-6].turn_on()
			self._mode_toggle[self._mode_index-6].send_value(7, True)
		else:
			self._mode_toggle[self._mode_index].turn_on()
		self._script.assign_page(self._mode_index)
		
	def disconnect(self):
		self._mode_toggle = None
		ModeSelectorComponent.disconnect(self)		


# local variables:
# tab-width: 4