'''
Created on Jan 1, 2013

@author: simonfuog
'''
from __future__ import with_statement
import Live
import time
from _Framework.ControlSurface import ControlSurface
from _Framework.InputControlElement import *
from _Framework.EncoderElement import EncoderElement
from OhmRGBMap import *
from OhmButton import OhmButton
from _Framework.MixerComponent import MixerComponent
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement
from _Framework.ButtonMatrixElement import ButtonMatrixElement
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from _Framework.TransportComponent import TransportComponent
from Shift import Shift
from PageModeComponent import PageModeComponent
from PlayPage import PlayPage
from SelectPage import SelectPage
from LogoPage import LogoPage
from TrackDeck import TrackDeck
from TrackRouter import TrackRouter
import math
from SessionOverwrite import SessionOverwrite

""" Global Stuff"""
FLK_FIRST_CLIPTRACK = 9
FLK_LAST_CLIPTRACK = 16

CHANNEL = 0 
switchxfader = (240, 00, 01, 97, 02, 15, 01, 247)
check_model = (240, 126, 127, 6, 1, 247)


class FluffyOhmNine(ControlSurface):
    '''
    classdocs
    '''


    def __init__(self,c_instance):
        ControlSurface.__init__(self, c_instance)
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------[ FluffyOhmNine log start ]--------------") # Writes message into Live's main log file. This is a ControlSurface method.
        #self.song().tracks[9].current_output_routing = "Sends Only"
        with self.component_guard():
            
            self._suppress_session_highlight = True
            self._suppress_send_midi = True
            is_momentary = True
            self._suggested_input_port = 'OhmRGB (Controls)'
            self._suggested_output_port = 'OhmRGB (Controls)'
            self._control_is_with_automap = False
            
            """ inst. variables"""        
            self.c_inst = c_instance
            self._rgb = 1
            self._timer = 0
            self.flash_status = 1
            self._backlight = 127
            self._backlight_type = 'static'
            self._ohm = 127
            self._ohm_type = 'static'
                          
            self._session_zoom = None
            self._session = None
            self._scene = None
            self._matrix = None
            self.main_mixer = None
            self.session_mixer = None
            self._transport = None
            
            self._trackdecks = [None,None,None,None]
            self._router = None
            #self._fx_section = None
            
            self.page_mode = None
            self.current_page = None
            self.shift = None
            self.shifted = False
            
            """ setup stuff starts here"""
            self._setup_controls()
            self._setup_fix_assignements()
            self._setup_session()
            self._setup_transport()
            
            self._setup_trackdecks()
            self._setup_router()
            
            #self.song().tracks[9].current_output_routing = "Sends Only"
            
            self._setup_shift()
            self._setup_pages()
            
#            self.assign_page(0)
#            self.assign_page(1)
#            self.assign_page(0)
            
            self.log_message("still here :)")
            
            self.schedule_message(10, self.query_ohm, None)

    def query_ohm(self):
        #self.log_message('querying Ohm')
        self._send_midi(tuple(check_model))            
        

    def _setup_controls(self):
        is_momentary = True
        self._fader = [None for index in range(8)]
        self._renc = [None for index in range(4)]
        self._enc = [None for index in range(12)]
        self._button = [None for index in range(8)]
        self._menu = [None for index in range(6)]
        for index in range(8):
            self._fader[index] = SliderElement(MIDI_CC_TYPE, CHANNEL, OHM_FADERS[index])
            self._fader[index].name = 'Fader_' + str(index), self
        for index in range(8):
            self._button[index] = OhmButton(is_momentary, MIDI_NOTE_TYPE, CHANNEL, OHM_BUTTONS[index], 'Button_' + str(index), self)
        for index in range(12):
            self._enc[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, OHM_DIALS[index], Live.MidiMap.MapMode.absolute)
            self._enc[index].name = 'Dial_' + str(index)
        for index in range(4):
            self._renc[index] = EncoderElement(MIDI_CC_TYPE, CHANNEL, OHM_DIALS[index+12], Live.MidiMap.MapMode.absolute)
            self._renc[index].name = 'RDial_' + str(index)
        for index in range(6):
            self._menu[index] = OhmButton(is_momentary, MIDI_NOTE_TYPE, CHANNEL, OHM_MENU[index], 'Menu_' + str(index), self)
            self._menu[index].menu_nr = index  
        self._crossfader = EncoderElement(MIDI_CC_TYPE, CHANNEL, CROSSFADER, Live.MidiMap.MapMode.absolute)
        self._crossfader.name = "Crossfader"
        self._shift = OhmButton(is_momentary, MIDI_NOTE_TYPE, CHANNEL, LIVID, 'Livid_Button', self)
        
        """ setup grid """
        self._matrix = ButtonMatrixElement()
        self._matrix.name = 'Matrix'
        self._grid = [None for index in range(8)]
        for column in range(8):
            self._grid[column] = [None for index in range(8)]
            for row in range(8):
                self._grid[column][row] = OhmButton(is_momentary, MIDI_NOTE_TYPE, CHANNEL, (column * 8) + row, 'Grid_' + str(column) + '_' + str(row), self)
                self._grid[column][row].set_grid_pos(column,row)
        for row in range(8):
            button_row = []
            for column in range(8):
                button_row.append(self._grid[column][row])
            self._matrix.add_row(tuple(button_row))



    def _setup_fix_assignements(self):
        
        """ 4 Ch Mixer with Fader and Solo """
        self._num_tracks = (4) #A mixer is one-dimensional; 
        self.main_mixer = MixerComponent(4, 0, False, False)
        self.main_mixer.name = 'Mixer'
        self.main_mixer.set_track_offset(0) #Sets start point for mixer strip (offset from left)
        for index in range(4):
            self.main_mixer.channel_strip(index).set_volume_control(self._fader[index])
        for index in range(4):
            self.main_mixer.channel_strip(index).name = 'Mixer_ChannelStrip_' + str(index)
            self.main_mixer.channel_strip(index).set_solo_button(self._button[index])
            self.main_mixer.channel_strip(index)._invert_mute_feedback = True

        """ 7 Ch Mixer for ClipTracks with Select and Solo """
        self._num_tracks = (7) #A mixer is one-dimensional; 
        self.session_mixer = MixerComponent(7, 0, False, False)
        self.session_mixer.name = 'Clip_Track_Mixer'
        self.session_mixer.set_track_offset(FLK_FIRST_CLIPTRACK) #Sets start point for mixer strip (offset from left)
        for index in range(7):
            #self.main_mixer.channel_strip(index).set_volume_control(self._fader[index])
            self.session_mixer.channel_strip(index).name = 'Clip_Track_Mixer_ChannelStrip_' + str(index)
            #self.main_mixer.channel_strip(index).set_solo_button(self._button[index])
            #self.main_mixer.channel_strip(index)._invert_mute_feedback = True

        
        """ Eq3 for Ch 1-4 """
        
   
    def _setup_transport(self):
        self._transport = TransportComponent() 
        self._transport.name = 'Transport'
     

    def _setup_session(self):
        #self.log_message("setup_session")

        self._suppress_session_highlight = True
        num_tracks = 7
        num_scenes = 6
        global session
        session = SessionOverwrite(num_tracks, num_scenes)
        session.name = "Session"
        self._session = session    
        session.set_offsets(FLK_FIRST_CLIPTRACK, 0)     
        self._scene = [None for index in range(6)]
        for row in range(num_scenes):
            self._scene[row] = session.scene(row)
            self._scene[row].name = 'Scene_' + str(row)
            for column in range(num_tracks):
                clip_slot = self._scene[row].clip_slot(column)
                clip_slot.name = str(column) + '_Clip_Slot_' + str(row)        
        session.set_mixer(self.session_mixer)
        self._session_zoom = SessionZoomingComponent(session)     
        self._session_zoom.name = 'Session_Overview'
        self._session.set_stop_track_clip_value(STOP_CLIP_COLOR[self._rgb])
        for row in range(num_scenes): 
            for column in range(num_tracks):
                self._scene[row].clip_slot(column).set_triggered_to_play_value(CLIP_TRIGD_TO_PLAY_COLOR[self._rgb])
                self._scene[row].clip_slot(column).set_triggered_to_record_value(CLIP_TRIGD_TO_RECORD_COLOR[self._rgb])
                self._scene[row].clip_slot(column).set_stopped_value(CLIP_STOPPED_COLOR[self._rgb])
                self._scene[row].clip_slot(column).set_started_value(CLIP_STARTED_COLOR[self._rgb])
                self._scene[row].clip_slot(column).set_recording_value(CLIP_RECORDING_COLOR[self._rgb])        
        self._session_zoom.set_stopped_value(ZOOM_STOPPED_COLOR[self._rgb])
        self._session_zoom.set_playing_value(ZOOM_PLAYING_COLOR[self._rgb])
        self._session_zoom.set_selected_value(ZOOM_SELECTED_COLOR[self._rgb])
        self._session_zoom.set_button_matrix(self._matrix)
        #self.song().view.add_selected_track_listener(self._update_selected_device)
        self._suppress_session_highlight = False
        self.set_highlighting_session_component(self._session)


    def _setup_trackdecks(self):
        for cnt in range(4):
            self._trackdecks[cnt] = TrackDeck(self)
        
    def _setup_router(self):
        self._router = TrackRouter(self)
        tr = self.song().tracks
        self._router.set_target_tracks(tr[0], tr[1], tr[2], tr[3])
        for cnt in range(FLK_LAST_CLIPTRACK - FLK_FIRST_CLIPTRACK):
            self._router.add_clip_track(tr[FLK_FIRST_CLIPTRACK+cnt])
        #self._router.setup_clip_tracks()
        

    def _setup_shift(self):
        self.shift = Shift(self)
        self.shift.set_mode_toggle(self._shift)
        

    def _setup_pages(self):
        self.page_mode = PageModeComponent(self)
        self.page_mode.set_mode_toggle(self._menu)
        
        
    def unshift_page(self):
        self.shifted = False
        if self.current_page != None:
            self.current_page.unshift_page()
        
    def shift_page(self):
        self.shifted = True
        if self.current_page != None:
            self.current_page.shift_page()
        
 
    def assign_page(self,page_nr):
        # called from Pagemodecomp
        if page_nr == 0:
            p = PlayPage(self)
            p.assign_page(self.current_page)
            
        elif page_nr == 1:
            p = SelectPage(self)
            p.assign_page(self.current_page)
            
        elif page_nr == 3:
            p = LogoPage(self)
            p.assign_page(self.current_page)
            
        else:
            if self.current_page != None:
                self.current_page.deassign_page()
            self.current_page = None

    def flash(self):
        for row in range(8):
            if(self._button[row]._flash_state > 0):
                self._button[row].flash(self._timer)
            for column in range(8):
                button = self._grid[column][row]
                if(button._flash_state > 0):
                    button.flash(self._timer)

    def strobe(self):
        if(self._backlight_type != 'static'):
            if(self._backlight_type is 'pulse'):
                self._backlight = int(math.fabs(((self._timer * 16) % 64) -32) +32)
            if(self._backlight_type is 'up'):
                self._backlight = int(((self._timer * 8) % 64) + 16)
            if(self._backlight_type is 'down'):
                self._backlight = int(math.fabs(int(((self._timer * 8) % 64) - 64)) + 16)
        self._send_midi(tuple([176, 27, int(self._backlight)]))
        if(self._ohm_type != 'static'):
            if(self._ohm_type is 'pulse'):
                self._ohm = int(math.fabs(((self._timer * 16) % 64) -32) +32)
            if(self._ohm_type is 'up'):
                self._ohm = int(((self._timer * 8) % 64) + 16)
            if(self._ohm_type is 'down'):
                self._ohm = int(math.fabs(int(((self._timer * 8) % 64) - 64)) + 16)
        self._send_midi(tuple([176, 63, int(self._ohm)]))
        self._send_midi(tuple([176, 31, int(self._ohm)]))
    
    def update_display(self):
        """ Live -> Script
        Aka on_timer. Called every 100 ms and should be used to update display relevant 
        parts of the controller
        """
#        for message in self._scheduled_messages:
#            message['Delay'] -= 1
#            if (message['Delay'] == 0):
#                if (message['Parameter'] != None):
#                    message['Message'](message['Parameter'])
#                else:
#                    message['Message']()
#                    del self._scheduled_messages[self._scheduled_messages.index(message)]
#
#        for callback in self._timer_callbacks:
#            callback()

        self._timer = (self._timer + 1) % 256
        self.flash()
        self.strobe()

            
    def disconnect(self):
        self._suppress_send_midi = True
        ControlSurface.disconnect(self)
        self._suppress_send_midi = False
        self.log_message(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()) + "--------------[ FluffyOhmNine log end ]--------------") # Writes message into Live's main log file. This is a ControlSurface method.



   