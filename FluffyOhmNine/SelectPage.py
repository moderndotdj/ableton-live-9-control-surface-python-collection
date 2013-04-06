'''
Created on Oct 2, 2012

@author: simonfuog
'''
from ShiftablePage import ShiftablePage
from OhmRGBMap import SCENE_LAUNCH_COLOR

class SelectPage(ShiftablePage):
    '''
    classdocs
    '''


    def __init__(self,parent):
        ShiftablePage.__init__(self,parent)
        self.never_shifted = True
    
        
    def assign_page(self, current_page):
        self.parent.log_message("assign_page:" + `self.__class__`)
        if current_page != None:
            current_page.deassign_page()
        #self.setup_session(6, 7)

        self.parent._backlight_type = 'static'
        self.parent._session_zoom.set_enabled(True)
        
        self.parent._session.select_page = self

        """ setup clip grid """
        for row in range(6):
            for column in range(7):
                self._scene[row].clip_slot(column).set_launch_button(self._grid[column][row])
            #self._grid[6][row+1]._off_value = SCENE_LAUNCH_COLOR[1]
            #self._grid[6][row+1]._on_value = SCENE_LAUNCH_COLOR[1] + 12
            
        self.lock_track()
        
        """ setup select btns """
        for col in range(7):
            self._grid[col][6].set_on_off_values(6,0)
            self.parent.session_mixer.channel_strip(col).set_select_button(self._grid[col][6])
        
        """ setup solo btns """
        for col in range(6):
            self.parent.session_mixer.channel_strip(col).set_solo_button(self._grid[col][7])
        
        """ setup nav btns """
        self._grid[7][7].set_on_off_values(3,3)
        self._grid[6][7].set_on_off_values(3,3)
        self._grid[7][6].set_on_off_values(3,3)
        self._grid[7][5].set_on_off_values(3,3)
        self.set_track_bank_buttons(self._grid[6][7], self._grid[7][7],True)
        self.set_scene_bank_buttons(self._grid[7][6], self._grid[7][5],True)
        self._grid[7][7].send_value(4)
        self._grid[6][7].send_value(4)
        self._grid[7][6].send_value(4)
        self._grid[7][5].send_value(4)
        
        """ setup route btns """
        self.parent._router.set_router_buttons([self._grid[7][0],self._grid[7][1],self._grid[7][2],self._grid[7][3]])
        
        
        
        self.parent.current_page = self
  
    def set_track_bank_buttons(self,r,l,x):
        if not x:
            r.remove_value_listener(self._right_value)
            l.remove_value_listener(self._left_value)
        else:
            r.add_value_listener(self._right_value,False)
            l.add_value_listener(self._left_value,False)
    
    def set_scene_bank_buttons(self,d,u,x):
        if not x:
            d.remove_value_listener(self._down_value)
            u.remove_value_listener(self._up_value)
        else:
            d.add_value_listener(self._down_value,False)
            u.add_value_listener(self._up_value,False)
            
    def _down_value(self,v):
        if v > 0:
            self.parent._session._bank_down()
            self.lock_track()
            self.parent._router.update_color()
    
    def _up_value(self,v):
        if v > 0:
            self.parent._session._bank_up()
            self.lock_track()
            self.parent._router.update_color()
        
    def _right_value(self,v):
        if v > 0: 
            if self.parent._session._track_offset > 9:
                self.parent._session._bank_left()
            self.lock_track()
            self.parent._router.update_color()
        
    def _left_value(self,v):
        #self.parent.log_message(`self.__class__` + "off" + `self.parent._session._track_offset`)
        if v > 0:
            self.parent._session._bank_right()
            self.lock_track()
            self.parent._router.update_color()
  
    
    def lock_track(self,x=0,y=0):
        """ lock tracks """
        track_decks = self.parent._trackdecks
        for row in range(6):
            for column in range(7):
                cs = self._scene[row].clip_slot(column)
                clip_track = cs._clip_slot.canonical_parent
                for td in track_decks:
                    if td._current_clip_track == clip_track:
                        if not td._live_track.mixer_device.volume.value == 0.0:
                            #cs.set_launch_button(None)
                            if cs._clip_slot.has_clip:
                                if cs._clip_slot.is_playing:
                                    self._grid[column+x][row+y].send_value(11)
                                else:
                                    self._grid[column+x][row+y].send_value(3)
                            else:
                                    self._grid[column+x][row+y].send_value(0)
                                
        
    def unlock_track(self,track):
        pass
    
        
    def deassign_page(self):
        #self.parent.request_rebuild_midi_map()
        #for index in range(6):
        #    self._scene[index].set_launch_button(None)
        for row in range(6):
            for column in range(7):
                self._scene[row].clip_slot(column).set_launch_button(None)
        for col in range(7):
            self.parent.session_mixer.channel_strip(col).set_select_button(None)
        for col in range(6):
            self.parent.session_mixer.channel_strip(col).set_solo_button(None)
        
        self.parent._router.set_router_buttons([None,None,None,None])
        self.set_track_bank_buttons(self._grid[7][7], self._grid[6][7],False)
        self.set_scene_bank_buttons(self._grid[7][6], self._grid[7][5],False)
        
        self.parent._session.select_page = None
        self.reset_btn_assignments()
        self.reset_btn_matrix()
        
        
        
        
    def shift_page(self):
        self.parent.log_message(`self.__class__` + "shift_page")
    
    def unshift_page(self):
        self.parent.log_message(`self.__class__` + "unshift_page")
  
  