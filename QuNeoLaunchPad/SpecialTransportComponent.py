import Live

from _Framework.TransportComponent import TransportComponent
from _Framework.ButtonElement import ButtonElement
from _Framework.EncoderElement import EncoderElement
from _Framework.InputControlElement import InputControlElement

from MIDI_Map import TEMPO_TOP
from MIDI_Map import TEMPO_BOTTOM

class SpecialTransportComponent(TransportComponent):
    __doc__ = ' TransportComponent that only uses certain buttons if a shift button is pressed '
    def __init__(self):
        TransportComponent.__init__(self)
        self._tempo_encoder_control = None
        self._tempo_down_button = None
        self._tempo_up_button = None
        self._tempo_session_value = self.song().tempo
        return None

    def disconnect(self):
        TransportComponent.disconnect(self)
        if (self._tempo_encoder_control != None): #new addition
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
            self._tempo_encoder_control = None
        if (self._tempo_down_button != None):
            self._tempo_down_button.remove_value_listener(self._tempo_down_value)
            self._tempo_down_button = None
        if (self._tempo_up_button != None):
            self._tempo_up_button.remove_value_listener(self._tempo_up_value)
            self._tempo_up_button = None
        return None

    def _tempo_encoder_value(self, value):
        assert (self._tempo_encoder_control != None)
        assert (value in range(128))
        backwards = (value >= 64)
        step = 0.1 #step = 1.0 #reduce this for finer control; 1.0 is 1 bpm
        if backwards:
            amount = (value - 128)
        else:
            amount = value
        tempo = max(20, min(999, (self.song().tempo + (amount * step))))
        self.song().tempo = tempo

    def _tempo_up_value(self, value):
        assert (value in range(128))
        assert (self._tempo_up_button != None)
        if (self.is_enabled()):
            if (value != 0):
                self._tempo_up_button.turn_on()
                new_tempo = 1.0
                real_tempo = (new_tempo + self.song().tempo)
                if real_tempo < 20.0:
                    real_tempo = 20.0
                self.update_tempo(real_tempo)
            else:
                self._tempo_up_button.turn_off()

    def _tempo_down_value(self, value):
        assert (value in range(128))
        assert (self._tempo_up_button != None)
        if (self.is_enabled()):
            if (value != 0):
                self._tempo_down_button.turn_on()
                new_tempo = -1.0
                real_tempo = (new_tempo + self.song().tempo)
                if (real_tempo > 200.0):
                    real_tempo = 200.0
                self.update_tempo(real_tempo)
            else:
                self._tempo_down_button.turn_off()

    def update_tempo(self, value):
        if (value != None):
            new_tempo = value
            self.song().tempo = new_tempo

    def set_tempo_buttons(self, up_button, down_button):
        assert ((up_button == None) or isinstance(up_button, ButtonElement))
        assert ((down_button == None) or isinstance(down_button, ButtonElement))
        if (self._tempo_up_button != None):
            self._tempo_up_button.remove_value_listener(self._tempo_up_value)
        self._tempo_up_button = up_button
        if (self._tempo_up_button != None):
            self._tempo_up_button.add_value_listener(self._tempo_up_value)
        if (self._tempo_down_button != None):
            self._tempo_down_button.remove_value_listener(self._tempo_down_value)
        self._tempo_down_button = down_button
        if (self._tempo_down_button != None):
            self._tempo_down_button.add_value_listener(self._tempo_down_value)
        self.update()

    def set_tempo_encoder(self, control):
        assert ((control == None) or (isinstance(control, EncoderElement) and (control.message_map_mode() is Live.MidiMap.MapMode.relative_two_compliment)))
        if (self._tempo_encoder_control != None):
            self._tempo_encoder_control.remove_value_listener(self._tempo_encoder_value)
        self._tempo_encoder_control = control
        if (self._tempo_encoder_control != None):
            self._tempo_encoder_control.add_value_listener(self._tempo_encoder_value)
        self.update()

    def _tempo_value(self, value): #Override to pull tempo range from MIDI_Maps.py
        assert (self._tempo_control != None)
        assert (value in range(128))
        if (self.is_enabled()):
            fraction = ((TEMPO_TOP - TEMPO_BOTTOM) / 127.0)
            self.song().tempo = ((fraction * value) + TEMPO_BOTTOM)
    
    def _stop_value(self, value):
        assert (self._stop_button != None)
        assert isinstance(value, int)
        if self.is_enabled():
            if ((value != 0) or (not self._stop_button.is_momentary())):
                self.song().is_playing = False
        if value>0:
            self._stop_button.turn_on()
        else:
            self._stop_button.turn_off()
