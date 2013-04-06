'''
Created on Sep 20, 2012

@author: simonfuog
'''
# emacs-mode: -*- python-*-
import Live
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent
from OhmButton import OhmButton

class Shift(ModeSelectorComponent):
    __module__ = __name__
    __doc__ = ' Special Class that uses two shift buttons and is lockable '

    def __init__(self, script):
        ModeSelectorComponent.__init__(self)
        self._script = script
        self._mode_toggle = None
        self._mode_index = 0

    def set_mode_toggle(self, shift_btn):
        if (self._mode_toggle != None):
            self._mode_toggle.remove_value_listener(self._toggle_value)
        self._mode_toggle = shift_btn
        if (self._mode_toggle != None):
            self._mode_toggle.add_value_listener(self._toggle_value,True)
        
        
        
        
        
        self._script.request_rebuild_midi_map()


        
    def _toggle_value(self, value, sender):
        assert isinstance(value, int)
        
        if value > 0:
            self.set_mode(1)
        else:
            self.set_mode(0)
            
    def number_of_modes(self):
        return 2

    def update(self):
        if self._mode_index == 0:
            self._mode_toggle.turn_off()
            self._script.unshift_page()
            self._script.page_mode._shift = False
        else:
            self._mode_toggle.turn_on()
            self._script.shift_page()
            self._script.page_mode._shift = True
        
        
    

    def set_mode(self, mode):
        assert isinstance(mode, int)
        assert (mode in range(self.number_of_modes()))
        if (self._mode_index != mode):
            self._mode_index = mode
            self.update()

# local variables:
# tab-width: 4