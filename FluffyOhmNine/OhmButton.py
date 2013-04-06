# emacs-mode: -*- python-*-
import Live
from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import InputControlElement
from _Framework.NotifyingControlElement import NotifyingControlElement
from OhmRGBMap import COLOR_MAP

#COLOR_MAP = [2, 64, 4, 8, 16, 127, 32]
MIDI_NOTE_TYPE = 0
MIDI_CC_TYPE = 1
MIDI_PB_TYPE = 2
MIDI_MSG_TYPES = (MIDI_NOTE_TYPE,
 MIDI_CC_TYPE,
 MIDI_PB_TYPE)
MIDI_NOTE_ON_STATUS = 144
MIDI_NOTE_OFF_STATUS = 128
MIDI_CC_STATUS = 176
MIDI_PB_STATUS = 224


class OhmButton(ButtonElement):
	__module__ = __name__
	__doc__ = ' Special button class that can be configured with custom on- and off-values, some of which flash at specified intervals called by _Update_Display'

	def __init__(self, is_momentary, msg_type, channel, identifier, name, cs):
		ButtonElement.__init__(self, is_momentary, msg_type, channel, identifier)
		self._flash_state = 0
		self._color = 0
		self._on_value = 127
		self._off_value = 0
		self._is_enabled = True
		self._is_notifying = False
		self._force_next_value = False
		self.name = name
		self._parameter = None
		self._script = cs
		self._report_value = True
		self.menu_nr = 0
		self.x = -1
		self.y = -1
		self.r = -1 # btn id for router
		self.cval = 0
		self._on = False
		self.fx = -1
#		self.tr_callback = None		
#		self.add_value_listener(self._btn_click)
#
#
#	def _btn_click(self,val):
#		if self.tr_callback !=None:
#			self.tr_callback.send_value(val)
#			#if self._on:
#			#	self.turn_off()
#			#else:
#			#	self.turn_on()
#


	def set_on_off_values(self, on_value, off_value):
		assert (on_value in range(128))
		assert (off_value in range(128))
		#self._last_sent_value = -1
		self._on_value = on_value
		self._off_value = off_value

	
	def set_grid_pos(self,x,y):
		self.x = x
		self.y = y
#
	def set_force_next_value(self):
		self._force_next_value = True

	def set_enabled(self, enabled):
		self._is_enabled = enabled
#
	def turn_on(self):
		self._on=True
		self.send_value(self._on_value)

	def turn_off(self):
		self._on=False
		self.send_value(self._off_value)

	def reset(self):
		self.send_value(0)
#		
#	def receive_value(self, value):
#		assert isinstance(value, int)
#		assert (value in range(128))
#		self._last_sent_value = -1
#		for notification in self._value_notifications:
#			callback = notification['Callback']
#			if notification['Identify']:
#				callback(value, self)
#			else:
#				callback(value)
#
	def send_value(self, value, force_send = False):		#commented this because of ButtonElement==NoneType errors in log
		if(type(self) != type(None)):
			assert (value != None)
			assert isinstance(value, int)
			assert (value in range(128))
			#value = 1
			self.cval = value
			if (force_send or ((value != self._last_sent_value) and self._is_being_forwarded)):
				data_byte1 = self._original_identifier
				if value in range(1, 127):
					data_byte2 = COLOR_MAP[(value - 1) % 6]
				elif value == 127:
					data_byte2 = COLOR_MAP[6]
				else:
					data_byte2 = 0
				self._color = data_byte2
				status_byte = self._original_channel
				if (self._msg_type == MIDI_NOTE_TYPE):
					status_byte += MIDI_NOTE_ON_STATUS
				elif (self._msg_type == MIDI_CC_TYPE):
					status_byte += MIDI_CC_STATUS
				else:
					assert False
				self.send_midi((status_byte,
				 data_byte1,
				 data_byte2))
				#self._last_sent_value = value
				if self._report_output:
					is_input = True
					self._report_value(value, (not is_input))
				self._flash_state = round((value -1)/7)
#
##	def install_connections(self):	#this override has to be here so that translation will happen when buttons are disabled
##		if self._is_enabled:
##			ButtonElement.install_connections(self)
##		elif ((self._msg_channel != self._original_channel) or (self._msg_identifier != self._original_identifier)):
##			self._install_translation(self._msg_type, self._original_identifier, self._original_channel, self._msg_identifier, self._msg_channel)
#
	def flash(self, timer):
		if (self._is_being_forwarded and self._flash_state in range(1, 18) and (timer % self._flash_state) == 0):
			data_byte1 = self._original_identifier
			data_byte2 = self._color * int((timer % (self._flash_state * 2)) > 0)
			status_byte = self._original_channel
			if (self._msg_type == MIDI_NOTE_TYPE):
				status_byte += MIDI_NOTE_ON_STATUS
			elif (self._msg_type == MIDI_CC_TYPE):
				status_byte += MIDI_CC_STATUS
			else:
				assert False
			self.send_midi((status_byte,
			 data_byte1,
			 data_byte2))
#			

# local variables:
# tab-width: 4
