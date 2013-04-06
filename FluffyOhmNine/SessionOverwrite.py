'''
Created on Jan 4, 2013

@author: simonfuog
'''
from _Framework.SessionComponent import SessionComponent

class SessionOverwrite(SessionComponent):
    '''
    overwrite to fix session area
    '''

    def __init__(self, num_tracks = 0, num_scenes = 0, *a, **k):
        super(SessionOverwrite, self).__init__( num_tracks, num_scenes, *a, **k)
        self.select_page = None
    
#    def _bank_up(self):
#        if not self.select_page == None:
#            self.select_page.lock_track(0,1)
#        return self.set_offsets(self.track_offset(), max(0, self.scene_offset() - 1))
#
#    
#    def _bank_down(self):
#        if not self.select_page == None:
#            self.select_page.lock_track(0,-1)
#        return self.set_offsets(self.track_offset(), self.scene_offset() + 1)
#
#    
#    def _bank_right(self):
#        if not self.select_page == None:
#            self.select_page.lock_track(-1,0)
#        return self.set_offsets(self.track_offset() + self._track_banking_increment, self.scene_offset())
#
#    
#    def _bank_left(self):
#        if not self.select_page == None:
#            self.select_page.lock_track(1,0)
#        return self.set_offsets(max(self.track_offset() - self._track_banking_increment, 0), self.scene_offset())
