import Live

from _Framework.ControlSurface import ControlSurface
from _Framework.ChannelStripComponent import ChannelStripComponent 
from ConfigurableButtonElement import *

TRACK_FOLD_DELAY = 5

class SpecialChannelStripComponent(ChannelStripComponent):
    ' Subclass of channel strip component using select button for (un)folding tracks '
    __module__ = __name__

    def __init__(self):
        ChannelStripComponent.__init__(self)
        self._reset_volume = None
        self._reset_pan = None
        self._reset_sendA = None
        self._reset_sendB = None
        self.mute_count = 0
        self._toggle_fold_ticks_delay = -1
        self._register_timer_callback(self._on_timer)

    def disconnect(self):
        if (self._reset_volume != None):
            self._reset_volume.remove_value_listener(self._reset_volume_value)
            self._reset_volume.reset()
            self._reset_volume = None
        self._unregister_timer_callback(self._on_timer)
        ChannelStripComponent.disconnect(self)
        return None

    def _select_value(self, value):
        ChannelStripComponent._select_value(self, value)
        if (self.is_enabled() and (self._track != None)):
            if (self._track.is_foldable and (self._select_button.is_momentary() and (value != 0))):
                self._toggle_fold_ticks_delay = TRACK_FOLD_DELAY
            else:
                self._toggle_fold_ticks_delay = -1

    def _on_timer(self):
        if (self.is_enabled() and (self._track != None)):
            if (self._toggle_fold_ticks_delay > -1):
                assert self._track.is_foldable
                if (self._toggle_fold_ticks_delay == 0):
                    self._track.fold_state = (not self._track.fold_state)
                self._toggle_fold_ticks_delay -= 1
                
    def reset_vol(self, button):
        assert (self._track != self.song().master_track)
        assert ((button == None) or isinstance(button, ConfigurableButtonElement))
        if (button != self._reset_volume):
            if (self._reset_volume != None):
                self._reset_volume.remove_value_listener(self._reset_volume_value)
                self._reset_volume.reset()
            self._reset_volume = False #added
            self._reset_volume = button
            if (self._reset_volume != None):
                self._reset_volume.add_value_listener(self._reset_volume_value)
                self._reset_volume.send_value(10)
            self.update()
            
    def _reset_volume_value(self, value):
        assert (self._reset_volume != None)
        assert (value in range(128))
        if (value > 0):
            self._track.mixer_device.volume.value = 0.85

    def reset_pan(self, button):
        assert (self._track != self.song().master_track)
        assert ((button == None) or isinstance(button, ConfigurableButtonElement))
        if (button != self._reset_pan):
            if (self._reset_pan != None):
                self._reset_pan.remove_value_listener(self._reset_pan_value)
                self._reset_pan.reset()
            self._reset_pan = False #added
            self._reset_pan = button
            if (self._reset_pan != None):
                self._reset_pan.add_value_listener(self._reset_pan_value)
                self._reset_pan.send_value(10)
            self.update()
            
    def _reset_pan_value(self, value):
        assert (self._reset_pan != None)
        assert (value in range(128))
        if (value > 0):
            self._track.mixer_device.panning.value = 0.0

    def reset_sendA(self, button):
        assert (self._track != self.song().master_track)
        assert ((button == None) or isinstance(button, ConfigurableButtonElement))
        if (button != self._reset_sendA):
            if (self._reset_sendA != None):
                self._reset_sendA.remove_value_listener(self._reset_sendA_value)
                self._reset_sendA.reset()
            self._reset_sendA = False #added
            self._reset_sendA = button
            if (self._reset_sendA != None):
                self._reset_sendA.add_value_listener(self._reset_sendA_value)
                self._reset_sendA.send_value(10)
            self.update()
            
    def _reset_sendA_value(self, value):
        assert (self._reset_sendA != None)
        assert (value in range(128))
        if (value > 0):
            self._track.mixer_device.sends[0].value = 0.0
            
    def reset_sendB(self, button):
        assert (self._track != self.song().master_track)
        assert ((button == None) or isinstance(button, ConfigurableButtonElement))
        if (button != self._reset_sendB):
            if (self._reset_sendB != None):
                self._reset_sendB.remove_value_listener(self._reset_sendB_value)
                self._reset_sendB.reset()
            self._reset_sendB = False #added
            self._reset_sendB = button
            if (self._reset_sendB != None):
                self._reset_sendB.add_value_listener(self._reset_sendB_value)
                self._reset_sendB.send_value(10)
            self.update()
            
    def _reset_sendB_value(self, value):
        assert (self._reset_sendB != None)
        assert (value in range(128))
        if (value > 0):
            self._track.mixer_device.sends[1].value = 0.0