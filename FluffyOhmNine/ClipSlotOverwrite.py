'''
Created on Jan 5, 2013

@author: simonfuog
'''
from _Framework.ClipSlotComponent import ClipSlotComponent

class ClipSlotOverwrite(ClipSlotComponent):
    '''
    classdocs
    '''


    def __init__(self, *a, **k):
        super(ClipSlotOverwrite, self).__init__(*a, **k)        
        self.deck = None
    
    def set_deck(self,d):
        self.deck = d
        
        
    def _on_playing_state_changed(self):
        self.update()

        self.deck.update()
        