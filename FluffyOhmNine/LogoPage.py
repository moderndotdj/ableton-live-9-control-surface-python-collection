'''
Created on Oct 2, 2012

@author: simonfuog
'''

import time
from ShiftablePage import ShiftablePage
from OhmRGBMap import SCENE_LAUNCH_COLOR, FLK_ANIMAP

class LogoPage(ShiftablePage):
    '''
    classdocs
    '''


    def __init__(self,parent):
        ShiftablePage.__init__(self,parent)
        self.never_shifted = True
    
        
    def assign_page(self, current_page):
        self.parent.log_message("assign_page Clip")
        if current_page != None:
            current_page.deassign_page()
        #self.setup_session(6, 7)

        for frame in range(8):
            time.sleep(0.25)
            for x in range(8):
                for y in range(8):
                    self._grid[x][y].send_value(FLK_ANIMAP[frame][y][x],True)
        
        for frame in range(8):
            time.sleep(0.25)
            for x in range(8):
                for y in range(8):
                    self._grid[x][y].send_value(FLK_ANIMAP[7 - frame][y][x],True)
        
        
        
        self.parent.current_page = self
        
        self.parent.shift.set_mode(0)
        self.parent.page_mode.set_mode(0)
        
    def deassign_page(self):
        self.reset_btn_matrix()
        #self.parent.request_rebuild_midi_map()
        
        
        
        
    def shift_page(self):
        self.parent.log_message(`self.__class__` + "shift_page")
    
    def unshift_page(self):
        self.parent.log_message(`self.__class__` + "unshift_page")
  
  