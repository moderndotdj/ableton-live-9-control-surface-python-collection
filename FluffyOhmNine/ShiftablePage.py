'''
Created on Oct 2, 2012

@author: simonfuog
'''
from _Framework.SessionComponent import SessionComponent
from _Framework.SessionZoomingComponent import SessionZoomingComponent
from OhmRGBMap import *

class ShiftablePage(object):
    '''
    classdocs
    '''


    def __init__(self,parent):
        self.parent = parent
        self._matrix = parent._matrix
        self._grid = parent._grid
        self._scene = parent._scene
        self._transport = parent._transport
        self._rgb = 1


    def assign_page(self, current_page):
        assert False
        
        
    def deassign_page(self):
        assert False
        
        
    def shift_page(self):
        assert False
    
    def unshift_page(self):
        assert False
    
    
    
    def reset_btn_matrix(self):
        #self.parent.log_message("reset_btn_matrix")
        #self._reset_grid_cell(7,0)
        self._matrix.reset()
        for column in range(8):
            for row in range(8):
                self._grid[column][row].set_channel(0)
                self._grid[column][row].release_parameter()
                self._grid[column][row].use_default_message()
                self._grid[column][row].set_enabled(True)
                self._grid[column][row].send_value(0, True)
                self._grid[column][row]._on_value = 127
                self._grid[column][row]._off_value = 0
                #self._grid[column][row]._remove_tr_callback()
        
        
        self.parent.request_rebuild_midi_map()
            
    def _reset_grid_cell(self,column,row):
        self._grid[column][row].set_channel(0)
        self._grid[column][row].release_parameter()
        self._grid[column][row].use_default_message()
        self._grid[column][row].set_enabled(True)
        self._grid[column][row].send_value(0, True)
        self._grid[column][row]._on_value = 127
        self._grid[column][row]._off_value = 0
  
        
    
    def _update_selected_device(self):
        x=12
    
    def reset_btn_assignments(self):
        self._transport.set_nudge_buttons(None,None)
        self._transport.set_metronome_button(None)
        self._transport.set_play_button(None)
        self.parent._session.set_scene_bank_buttons(None,None)
        
    def set_nudge_btn(self,x,y):
        n_up = self._grid[x+1][y]
        n_up.turn_on()
        n_up.set_on_off_values(1,127)
        n_down = self._grid[x][y]
        n_down.turn_on()
        n_down.set_on_off_values(1,127)
        self._transport.set_nudge_buttons(n_up,n_down)
        
    def set_metro_btn(self,x,y):
        metro = self._grid[x][y]
        if self.parent.song().metronome:
            metro.turn_on()
        metro.set_on_off_values(8,2)
        self._transport.set_metronome_button(metro)        
    
    def set_play_btn(self,x,y):
        ply = self._grid[x][y]
        if self.parent.song().is_playing:
            ply.turn_on()
        ply.set_on_off_values(6,0)
        self._transport.set_play_button(ply)
        
    def set_session_nav(self,x,y):
        self.parent._session.set_scene_bank_buttons(self._grid[x][y+1],self._grid[x][y])
        
