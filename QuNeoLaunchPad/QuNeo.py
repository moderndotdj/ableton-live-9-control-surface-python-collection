# VERSION 1.0



# Copyright 7/3/2012
# Control Surface Remote Script Created by Alex Molina 
# for QuNeo 3D MultiTouch Pad Controller by Keith McMillen Instruments
# TESTED DEVICE = QUENEO SERIAL #104998

from __future__ import with_statement

import Live
import time
import math

from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonSliderElement import ButtonSliderElement
from _Framework.DeviceComponent import DeviceComponent
from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.CompoundComponent import CompoundComponent
from _Framework.EncoderElement import EncoderElement
from _Framework.ControlElement import ControlElement
from _Framework.ControlSurface import ControlSurface
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
from _Framework.InputControlElement import *
from _Framework.SceneComponent import SceneComponent
from _Framework.SliderElement import SliderElement
from _Framework.ModeSelectorComponent import ModeSelectorComponent

from SpecialChannelStripComponent import *
from DetailViewControllerComponent import DetailViewControllerComponent
from ShiftModeComponent import ShiftModeComponent
from ConfigurableButtonElement import ConfigurableButtonElement
from SpecialModeSelectorComponent import SpecialModeSelectorComponent
from SpecialSessionComponent import SpecialSessionComponent
from SpecialTransportComponent import SpecialTransportComponent
from SpecialMixerComponent import SpecialMixerComponent
from ConfigurableButtonSlider import ConfigurableButtonSlider

from MIDI_Map import *
from VUMeter import VUMeter

session = None
mixer = None
check_model = (240, 126, 127, 6, 1, 247)

class QuNeo(ControlSurface):
    __doc__ = " Script for Keith McMillen's QuNeo Multi-Touchpad Controller "
    __module__ = __name__
    _active_instances = []
    def _combine_active_instances():
        support_devices = False
        for instance in QuNeo._active_instances:
            support_devices |= instance._device_component != None
        track_offset = 0
        for instance in QuNeo._active_instances:
            instance._activate_combination_mode(track_offset, support_devices)
            track_offset += instance._session.width()
        return None
        
    _combine_active_instances = staticmethod(_combine_active_instances)
    
    # INIT FUNCTION FOR QUNEO   
    def __init__(self, c_instance):
        ControlSurface.__init__(self, c_instance)
        with self.component_guard():
          self._suggested_input_port = 'QUNEO'
          self._suggested_output_port = 'QUNEO'
          self.session = None
          self.mixer = None
          self.shift_mode = None
          self.transport = None
          self.shift_button = None
          self.shift_buttons = []
          self.reset_vol = []
          self.sends = []
          self.clip = []
          self.clip_slot_buttons = None
          self.stop_track_buttons = []
          self.vol_button_slider = None
          self._vol_bslider = None
          self.reset_volume = []
          self.reset_pan = []
          self.reset_sendA = []
          self.reset_sendB = []
          self.seq_offset_left = None
          self.seq_offset_right = None
          self.seq_offset_up = None
          self.seq_offset_down = None
          self.sequencer_buttons = []
          self.volume_control = None
          self.pan_control = None
          self.current_mode = 0
          self._setup_controls()
          self._setup_transport_control()
          self._setup_mixer_control()
          self._setup_session_control()
          self._setup_device_control()
          self._setup_modes()
          self.session.set_mixer(self.mixer)
          self.set_highlighting_session_component(self.session)
          self._suppress_session_highlight = False
          
          """ Here is some Live API stuff just for fun """
          app = Live.Application.get_application() # get a handle to the App
          maj = app.get_major_version() # get the major version from the App
          min = app.get_minor_version() # get the minor version from the App
          bug = app.get_bugfix_version() # get the bugfix version from the App
          self.show_message(str(maj) + "." + str(min) + "." + str(bug)) #put them together and use the ControlSurface show_message method to output version info to console
  #         self.log_message("SCRIPT LOADED")
          self.schedule_message(100, self.refresh_state, None)
          self.show_message("cats")
        
    # DISCONNECT FUNCTION
    def disconnect(self):
        self.mixer
        self.session
#         self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------= QUNEO CLOSED LED =--------------") # Writes message into Live's main log file. This is a ControlSurface method.
        ControlSurface.disconnect(self)
    
    # CLIP LAUNCHING MODE
    def _update_grid(self):
        self.transport.set_metronome_button(self.led_button(PAD_CHANNEL, METRONOME, 127))# Metronome Button
        self.transport.set_play_button(self.led_button(PAD_CHANNEL, PLAY, 127))#Play Button
        self.transport.set_stop_button(self.led_button(PAD_CHANNEL, STOP, 127))#Stop Button
        self.transport.set_record_button(self.led_button(PAD_CHANNEL, REC,127))#Record Button
        self.transport.set_overdub_button(self.led_button(PAD_CHANNEL, OVERDUB, 127))# Overdub Button
        self.transport.set_tempo_buttons(self.led_button(PAD_CHANNEL, TEMPO_UP, 127), self.led_button(PAD_CHANNEL, TEMPO_DOWN, 127))
        self.transport.set_seek_buttons(self.led_button(PAD_CHANNEL, SEEKFWD, 127), self.led_button(PAD_CHANNEL, SEEKRWD, 127))
        self.transport.set_loop_button(self.led_button(PAD_CHANNEL, LOOP, 127))# Loop Button
        self.transport.set_tap_tempo_button(self.led_button(PAD_CHANNEL, TAP_TEMPO, 127))#Tap Tempo
        
        self.clip_slot_buttons = []
        for row in range(8):
            self.clip_slot_buttons.append([])
            for col in range(8):
                self.clip_slot_buttons[row].append(self.button(GRID_CHANNEL, CLIP_NOTE_MAP[row][col]))
        for row in range(8):
            for col in range(8):
                self.clip = self.session.scene(row).clip_slot(col)
                if (self.clip_slot_buttons != None):
                    self.clip.set_triggered_to_play_value(30)
                    self.clip.set_triggered_to_record_value(RED_HI)
                    self.clip.set_started_value(30)
                    self.clip.set_recording_value(RED_HI)
                    self.clip.set_stopped_value(80)
                    self.clip.set_triggered_to_record_value(6)
                    self.clip.set_launch_button(self.clip_slot_buttons[row][col])
                else:
                    self.clip.set_launch_button(None)
                    
        for index in range(4):
            self.mixer.channel_strip(index).set_volume_control(self.slider(SLIDER_CHANNEL, TRACK_VOL[index]))
            
        self._on_selected_track_changed()
        
    # DEASSIGN ALL BUTTONS
    def _disable_buttons(self):
        if (self._vol_bslider != None or self._vol_bslider > 1):
            for row in range(len(self._vol_bslider)):
                self._vol_bslider[row].release_parameter()
                self._vol_bslider[row].disconnect()
            self._vol_bslider = None
            
        if (self.vol_button_slider != None):
            for row in range(len(self.vol_button_slider)):
                for col in range(len(self.vol_button_slider[row])):
                    self.vol_button_slider[row][col].release_parameter()
                    self.vol_button_slider[row][col].disconnect()
            self.vol_button_slider = None
            
        if (self.sequencer_buttons != None):
            for button in self.sequencer_buttons:
                button.turn_off()
                button.count = 0
        self.sequencer_buttons = None
        self.session.set_sequencer_buttons(None)
        
        self.track_bank_left = None
        self.track_bank_right = None
        self.scene_bank_up = None
        self.scene_bank_down = None
        self.seq_offset_left = None
        self.seq_offset_right = None
        self.seq_offset_up = None
        self.seq_offset_down = None
        
        for row in range(8):
            for col in range(8):
                self.clip_slot_buttons[row][col].turn_off()
                self.mixer.channel_strip(row).set_mute_button(None)
                self.stop_track_buttons.append(None)
                self.session.set_stop_track_clip_buttons(None)
                self.mixer.channel_strip(row).set_solo_button(None)
                self.mixer.channel_strip(row).set_arm_button(None)
                self.mixer.channel_strip(row).set_volume_control(None)
                self.mixer.channel_strip(row).set_pan_control(None)
                self.mixer.channel_strip(row).set_send_controls(tuple([None, None]))
                self.mixer.channel_strip(row).reset_vol(None)
                self.mixer.channel_strip(row).reset_pan(None)
                self.mixer.channel_strip(row).reset_sendA(None)
                self.mixer.channel_strip(row).reset_sendB(None)
                
        for row in range(8):
            for col in range(8):
                self.clip = self.session.scene(row).clip_slot(col)
                if (self.clip_slot_buttons != None):
                    self.clip.set_launch_button(None)
                else:
                    None
                    
    # MIXER MODE
    def _mixer_mode(self):
        self.stop_track_buttons = []
        for row in range(8):
            self.mixer.channel_strip(row).set_invert_mute_feedback(True)
            self.mixer.channel_strip(row).set_mute_button(self.led_button(GRID_CHANNEL, TRACK_MUTE[row], GREEN_HI))
            self.stop_track_buttons.append(self.led_button(GRID_CHANNEL, STOP_TRACK[row], RED_HI))
            self.mixer.channel_strip(row).set_solo_button(self.led_button(GRID_CHANNEL, TRACK_SOLO[row], ORANGE_HI))
            self.mixer.channel_strip(row).set_arm_button(self.led_button(GRID_CHANNEL, TRACK_ARM[row], RED_HI))
        self.session.set_stop_track_clip_buttons(tuple(self.stop_track_buttons))
        
        for index in range(4):
            self.mixer.channel_strip(index).set_volume_control(self.slider(SLIDER_CHANNEL, TRACK_VOL[index]))
            
        self.reset_volume = []
        self.reset_pan = []
        self.reset_sendA = []
        self.reset_sendB = []
        for row in range(8):
            self.reset_volume.append(self.led_button(GRID_CHANNEL, CLIP_NOTE_MAP[0][row], GREEN_LO))
            self.reset_pan.append(self.led_button(GRID_CHANNEL, CLIP_NOTE_MAP[1][row], GREEN_LO))
            self.reset_sendA.append(self.led_button(GRID_CHANNEL, CLIP_NOTE_MAP[2][row], GREEN_LO))
            self.reset_sendB.append(self.led_button(GRID_CHANNEL, CLIP_NOTE_MAP[3][row], GREEN_LO))
        for row in range(8):
            self.mixer.channel_strip(row).reset_vol(self.reset_volume[row])
            self.mixer.channel_strip(row).reset_pan(self.reset_pan[row])
            self.mixer.channel_strip(row).reset_sendA(self.reset_sendA[row])
            self.mixer.channel_strip(row).reset_sendB(self.reset_sendB[row])

    # BUTTON SLIDER MIXER MODE
    def _volume_mode(self, type):
        self.vol_button_slider = []
        for row in range(8):
            self.vol_button_slider.append([])
            for col in range(8):
                self.vol_button_slider[row].append(self.button(GRID_CHANNEL, BUTTONSLIDER[row][col]))
        self._vol_bslider = []
        for row in range(8):
            self._vol_bslider.append(ConfigurableButtonSlider(tuple(self.vol_button_slider[row])))
        for row in range(8):
            if type == 0:
                self.mixer.channel_strip(row).set_volume_control(self._vol_bslider[row])
            elif type == 1:
                self.mixer.channel_strip(row).set_pan_control(self._vol_bslider[row])
            elif type == 2:
                self.mixer.channel_strip(row).set_send_controls(tuple([self._vol_bslider[row], None]))
            elif type == 3:
                self.mixer.channel_strip(row).set_send_controls(tuple([None, self._vol_bslider[row]]))
                
    def _step_sequencer(self):
        self.sequencer_buttons = []
        self.seq_offset_left = self.button(PAD_CHANNEL, SESSION_LEFT)
        self.seq_offset_right = self.button(PAD_CHANNEL, SESSION_RIGHT)
        self.seq_offset_up = self.button(PAD_CHANNEL, SESSION_UP)
        self.seq_offset_down = self.button(PAD_CHANNEL, SESSION_DOWN)
        for row in range(8):
                for col in range(8):
                    self.sequencer_buttons.append(self.led_button(GRID_CHANNEL, CLIP_NOTE_MAP[row][col], GREEN_HI))
        self.session.set_sequencer_buttons(self.sequencer_buttons)
        self.session.clear_led()
        self.session.update_notes()
        self.session.on_device_changed()
            
    # CREATE A BUTTON
    def button(self, channel, value):
        is_momentary = True
        if (value != -1):
            return ButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, value)
        else:
            return None
            
    # CREATE A LED BUTTON
    def led_button(self, channel, value, vel):
        is_momentary = True
        if (value != -1):
            return ConfigurableButtonElement(is_momentary, MIDI_NOTE_TYPE, channel, value, vel)
        else:
            return None
            
    # CREATE A SLIDER
    def slider(self, channel, value):
        if (value != -1):
            return SliderElement(MIDI_CC_TYPE, channel, value)
        else:
            return None
            
    # CREATE AN ENCODER
    def assign_encoder(self, channel, value):
        if (value != -1):
            return EncoderElement(MIDI_CC_TYPE, channel, value, Live.MidiMap.MapMode.relative_two_compliment)
        else:
            return None
            
    # SETUP SHIFT BUTTON
    def _setup_controls(self):
        self.shift_button = ConfigurableButtonElement(True, MIDI_NOTE_TYPE, PAD_CHANNEL, SHIFT_BUTTON, 127)

    # SETUP TRANSPORT CONTROL
    def _setup_transport_control(self):
        self.transport = SpecialTransportComponent()
        self.transport.set_metronome_button(self.led_button(PAD_CHANNEL, METRONOME, 127))# Metronome Button
        self.transport.set_play_button(self.led_button(PAD_CHANNEL, PLAY, 127))#Play Button
        self.transport.set_stop_button(self.led_button(PAD_CHANNEL, STOP, 127))#Stop Button
        self.transport.set_record_button(self.led_button(PAD_CHANNEL, REC,127))#Record Button
        self.transport.set_overdub_button(self.led_button(PAD_CHANNEL, OVERDUB, 127))# Overdub Button
        self.transport.set_tempo_buttons(self.led_button(PAD_CHANNEL, TEMPO_UP, 127), self.led_button(PAD_CHANNEL, TEMPO_DOWN, 127))
        self.transport.set_seek_buttons(self.led_button(PAD_CHANNEL, SEEKFWD, 127), self.led_button(PAD_CHANNEL, SEEKRWD, 127))
        self.transport.set_loop_button(self.led_button(PAD_CHANNEL, LOOP, 127))# Loop Button
        self.transport.set_tap_tempo_button(self.led_button(PAD_CHANNEL, TAP_TEMPO, 127))#Tap Tempo
        
    # SETUP MIXER
    def _setup_mixer_control(self):
        self.mixer = SpecialMixerComponent(8, self)
        self.mixer.name = 'Mixer'
        self.mixer.set_track_offset(0)
        self.mixer.set_select_buttons(self.button(PAD_CHANNEL, TRACK_RIGHT), self.button(PAD_CHANNEL, TRACK_LEFT)) #left, right track select      
        self.mixer.set_crossfader_control(self.slider(SLIDER_CHANNEL, CROSSFADER))
        
        for index in range(2):
            self.sends.append(self.slider(SLIDER_CHANNEL, SELECTED_SENDS[index]))
        self.volume_control = self.slider(SLIDER_CHANNEL, SELECTED_VOL)
        self.pan_control = self.slider(SLIDER_CHANNEL, SELECTED_PAN)
        
        self.mixer.selected_strip().set_send_controls(tuple(self.sends))
        self.mixer.selected_strip().set_volume_control(self.volume_control)
        self.mixer.selected_strip().set_pan_control(self.pan_control)

        for index in range(4):
            self.mixer.channel_strip(index).set_volume_control(self.slider(SLIDER_CHANNEL, TRACK_VOL[index]))
        
        #VU METERS
        self.num_o_tracks = self.song().visible_tracks
        if (self.num_o_tracks != None):
            index_count = -1
            index_table = []
            for index in self.song().visible_tracks:
                index_count += 1
                if (index.has_midi_output != True):
                    index_table.append(index_count)
                else:
                    None
            if (index_table != None):
                for index in range(len(index_table)):
                    x = index_table[index]
                    if (x > 3):
                        None
                    else:
                        None
#                         self.mixer.vu_meter(index).set_vu_meter(index_table[index])

    # SETUP SESSION
    def _setup_session_control(self):
        self.session = SpecialSessionComponent(8, 8, self)
        self.session.set_offsets(0, 0)
        self.session.set_select_buttons(self.led_button(PAD_CHANNEL, SCENE_DOWN, 127), self.led_button(PAD_CHANNEL, SCENE_UP, 127))
        self.session.set_track_bank_buttons(self.led_button(PAD_CHANNEL, SESSION_RIGHT, 127), self.led_button(PAD_CHANNEL, SESSION_LEFT, 127))
        self.session.set_scene_bank_buttons(self.led_button(PAD_CHANNEL, SESSION_UP, 127), self.led_button(PAD_CHANNEL, SESSION_DOWN, 127))
        
        self.clip_slot_buttons = []
        for row in range(8):
            self.clip_slot_buttons.append([])
            for col in range(8):
                self.clip_slot_buttons[row].append(self.led_button(GRID_CHANNEL, CLIP_NOTE_MAP[row][col], 127))
                
        for row in range(8):
            for col in range(8):
                self.clip = self.session.scene(row).clip_slot(col)
                if (self.clip_slot_buttons != None):
                    self.clip.set_triggered_to_play_value(30)
                    self.clip.set_triggered_to_record_value(RED_HI)
                    self.clip.set_started_value(30)
                    self.clip.set_recording_value(RED_HI)
                    self.clip.set_stopped_value(80)
                    self.clip.set_triggered_to_record_value(6)
                    self.clip.set_launch_button(self.clip_slot_buttons[row][col])
                    
    # SETUP DEVICE CONTROL
    def _setup_device_control(self):
        self._device = DeviceComponent()
#         self._device.set_lock_button(self.led_button(NOTE_OFFSET, DEVICELOCK, 127))
        detail_view_toggler = DetailViewControllerComponent()
        detail_view_toggler.set_device_clip_toggle_button(self.led_button(NOTE_OFFSET, DEVICELOCK, 127))
        detail_view_toggler.set_device_nav_buttons(self.led_button(NOTE_OFFSET, DEVICENAVLEFT, 127), self.led_button(NOTE_OFFSET, DEVICENAVRIGHT, 127))
    
    # SETUP MODE COMPONENT
    def _setup_modes(self):
        self._shift_mode = ShiftModeComponent(self) 
        self._shift_mode.name = 'Shift_Mode'
        self._shift_mode.set_mode_hold(self.shift_button)
    
    # HANDSHAKE QUNEO
    def handle_sysex(self, midi_bytes):
        if (midi_bytes[15] == 8):
            self.log_message("PRESET 8"+ str(midi_bytes))
            self.check_mode_state()
        elif (midi_bytes[15] == 9):
            self._disable_buttons()
            self.log_message("PRESET 9"+ str(midi_bytes))
        else:
            None
            
    # CHECK MODE TO RELIGHT LEDS AFTER QUNEO IS PLUGGED IN
    def check_mode_state(self):
        if (self.current_mode == 0):
            self._disable_buttons()
            self._update_grid()# UPDATE GRID
        elif (self.current_mode == 1):
            self._disable_buttons()
            self._mixer_mode()# MIXER MODE
        elif (self.current_mode == 2):
            self._disable_buttons()
            self._volume_mode(0)# VOLUME 
        elif (self.current_mode == 3):
            self._disable_buttons()
            self._volume_mode(1)# PAN
        elif (self.current_mode == 4):
            self._disable_buttons()
            self._volume_mode(2)# SEND A
        elif (self.current_mode == 5):
            self._disable_buttons()
            self._volume_mode(3)# SEND B
        elif (self.current_mode == 6):
            self._disable_buttons()
            self._step_sequencer()# STEP SEQUENCER
        elif (self.current_mode == 7):
            self._disable_buttons()
            self._user_mode(1)
        else:
            None
            
    # REFRESH QUNEO (RELIGHT LEDS)
    def refresh_state(self):
        #self.set_suppress_rebuild_requests(True)
        self._suggested_input_port = 'QUNEO'
        if (self._suggested_input_port == 'QUNEO'):
            self._send_midi((240, 0, 1, 95, 122, 30, 0, 1, 0, 2, 80, 4, 36, 27, 0, 48, 247))
        else:
            self.log_message("FALSE")
        #self.set_suppress_rebuild_requests(False)
        
    def _on_selected_scene_changed(self):
        ControlSurface._on_selected_scene_changed(self)
        
    def _on_selected_track_changed(self):
        ControlSurface._on_selected_track_changed(self)
        
    def _activate_combination_mode(self, track_offset, support_devices):
        self._session.link_with_track_offset(track_offset)
        
