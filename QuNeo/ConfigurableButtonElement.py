import Live

from _Framework.ButtonElement import *

class ConfigurableButtonElement(ButtonElement):
    __module__ = __name__
    __doc__ = ' Special button class that can be configured with custom on- and off-values '

    def __init__(self, is_momentary, msg_type, channel, identifier, vel):
        ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
        if vel != 0:
        	self._on_value = vel #127 for Launchpad #0=off, 1=green, 2=green blink, 3=red, 4=red blink, 5=yellow, 6=yellow blink, 7-127=green
        else:
        	self._on_value = 127
        self._note = identifier
        self._off_value = 0 #4 for Launchpad, 0 for APC40/20
        self._blink_on = None
        self._blinking = False
        self._led_on = 0
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False
        self._pending_listeners = []
        self.count = 0

    def note_on(self):
        if (self.count > 1):
            self.count = 0
        else:
            None
        if (self.count == 1):
            self.turn_on()
        else:
            self.turn_off()

    def set_on_off_values(self, on_value, off_value):
        assert (on_value in range(128))
        assert (off_value in range(128))
        self._last_sent_value = -1
        self._on_value = on_value
        self._off_value = off_value

    def set_force_next_value(self):
        self._force_next_value = True

    def set_enabled(self, enabled):
        self._is_enabled = enabled

    def turn_on(self):
        self.send_value(self._on_value)

    def turn_off(self):
        self.send_value(self._off_value)

    def reset(self):
        self.send_value(0) #4 for Launchpad, 0 for APC40/20

    def add_value_listener(self, callback, identify_sender = False):
        if (not self._is_notifying):
            ButtonElement.add_value_listener(self, callback, identify_sender)
        else:
            self._pending_listeners.append((callback, identify_sender))

    def receive_value(self, value):
        self._is_notifying = True
        ButtonElement.receive_value(self, value)
        
        self._is_notifying = False
        for listener in self._pending_listeners:
            self.add_value_listener(listener[0], listener[1])

        self._pending_listeners = []

    def send_value(self, value, force = False):
        ButtonElement.send_value(self, value, (force or self._force_next_value))
        self._force_next_value = False
        
    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        if self._is_enabled:
            ButtonElement.install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback)
        elif self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
            install_translation_callback(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)
