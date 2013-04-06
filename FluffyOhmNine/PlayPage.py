'''
Created on Oct 2, 2012

@author: simonfuog
'''
from ShiftablePage import ShiftablePage
from OhmRGBMap import SCENE_LAUNCH_COLOR


class PlayPage(ShiftablePage):
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
        
        startx = [0,2,4,6]
        for cnt in range(4):
            self.parent._trackdecks[cnt].set_deck_btns(self._grid,startx[cnt],cnt)
            self.parent._router._update_deck_clip(cnt)

        
        
        
        self.parent.current_page = self
        
    def deassign_page(self):
        
        for cnt in range(4):
            self.parent._trackdecks[cnt].set_deck_btns(None,None,None)
        
        self.reset_btn_matrix()
        #self.parent.request_rebuild_midi_map()
        
        
        
        
    def shift_page(self):
        self.parent.log_message(`self.__class__` + "shift_page")
        for d in self.parent._trackdecks:
            d._shift = True
    
    def unshift_page(self):
        self.parent.log_message(`self.__class__` + "unshift_page")
        for d in self.parent._trackdecks:
            d._shift = False
  