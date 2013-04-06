'''
Created on Jan 3, 2013

@author: simonfuog
'''
from _Framework.ClipSlotComponent import ClipSlotComponent
from ClipSlotOverwrite import ClipSlotOverwrite
from FxSection import FxStrip

class TrackDeck(object):

    """ this class exposes the functionality of a Deck """
    def __init__(self,script):
        self.parent = script
        self._live_track = None
        self._live_track_input = None
        self._current_clip = None
        self._current_clip_track = None
        self._cross_track = None
        
        self._deck_grid = [None for index in range(16)]
        self._shift = False
        self._display = False
        
        self._clip = None
        self._clip_slot = None
        self._steps = [1.0,4.0,16.0]
        self._step_colors = [1,3,4,4,3]
        self._step_size = 1
        
        self._fx_strip = None 
        

    def set_deck_btns(self,full_grid,start_x,track_nr):
        if self._live_track == None:
            """ setup ref to track """
            self._live_track = self.parent.song().tracks[track_nr]
            self._cross_track = self.parent.song().tracks[track_nr+5]
        if self._fx_strip == None:
            self._fx_strip = FxStrip(self,self._live_track,self.parent._fader[track_nr+4],self.parent._renc[track_nr],self.parent._button[track_nr+4],track_nr)

        
        if full_grid == None:
            """ tear down (let go of btns) """
            """ remove listeners """
            self._deck_grid[0].remove_value_listener(self._btn_loop_toggl)
            self._deck_grid[1].remove_value_listener(self._btn_step_size)
            self._deck_grid[2].remove_value_listener(self._btn_dec_loop)
            self._deck_grid[3].remove_value_listener(self._btn_mv_loop_left)
            self._deck_grid[4].remove_value_listener(self._btn_zoom)
            self._deck_grid[8].remove_value_listener(self._btn_clip_play)
            self._deck_grid[9].remove_value_listener(self._btn_clip_stop)
            self._deck_grid[10].remove_value_listener(self._btn_inc_loop)
            self._deck_grid[11].remove_value_listener(self._btn_mv_loop_right)
            self._deck_grid[12].remove_value_listener(self._btn_xfade)
            self._fx_strip.set_btns(None)
            self._display = False         
        
        else:
            
            self._display = True
        
            """ get a block of 16 btns for deck """
            for cnt in range(16):
                if cnt < 8:
                    self._deck_grid[cnt] = full_grid[start_x][cnt]
                else:
                    self._deck_grid[cnt] = full_grid[start_x + 1][cnt - 8]
        
            """ add listeners """
            self._deck_grid[0].add_value_listener(self._btn_loop_toggl)
            self._deck_grid[0].send_value(self._loop_btn_color())
            self._deck_grid[1].add_value_listener(self._btn_step_size,True)
            self._deck_grid[1].send_value(self._step_colors[self._step_size])
            self._deck_grid[2].add_value_listener(self._btn_dec_loop)
            self._deck_grid[2].send_value(self._step_colors[self._step_size])
            self._deck_grid[3].add_value_listener(self._btn_mv_loop_left)
            self._deck_grid[3].send_value(self._step_colors[self._step_size+2])
            self._deck_grid[4].add_value_listener(self._btn_zoom)
            self._deck_grid[4].send_value(127)
            self._deck_grid[8].add_value_listener(self._btn_clip_play)
            self._deck_grid[8].send_value(self._play_btn_color())
            self._deck_grid[9].add_value_listener(self._btn_clip_stop)
            self._deck_grid[9].send_value(self._stop_btn_color())
            self._deck_grid[10].add_value_listener(self._btn_inc_loop)
            self._deck_grid[10].send_value(self._step_colors[self._step_size])
            self._deck_grid[11].add_value_listener(self._btn_mv_loop_right)
            self._deck_grid[11].send_value(self._step_colors[self._step_size+2])
            self._deck_grid[12].add_value_listener(self._btn_xfade)
            self._fx_strip.set_btns([self._deck_grid[5],self._deck_grid[13],self._deck_grid[6],self._deck_grid[14],self._deck_grid[15],self._deck_grid[7]])

    def set_cross_signal(self,v):
        if v:
            self._cross_track.mixer_device.volume.value = 0.0
        else:
            self._cross_track.mixer_device.volume.value = 0.85
            

    def set_clip(self,clip_slot,clip_track):
        if clip_slot == None and clip_track == None:
            if self._clip == None:
                pass
            else:
                #self._clip.remove_playing_status_listener(self._clip_play_value)
                pass
            self._clip = None
            self._clip_slot = None
            self._current_clip_track = None
        else:
            self._clip = clip_slot.clip
            cs = ClipSlotOverwrite()
            cs.set_deck(self)
            cs.set_clip_slot(clip_slot)
            self._clip_slot = cs
            self._current_clip_track = clip_track
            
            #self._clip.add_playing_status_listener(self._clip_play_value)
    
    def update(self):
        if self._display:
            #self.parent.log_message("playing_status" + `self._clip.is_triggered` + `self._clip.is_playing` + `self._clip_slot._clip_slot.playing_status`)
            self._deck_grid[8].send_value(self._play_btn_color())
            self._deck_grid[9].send_value(self._stop_btn_color())
      

     
    """ Btn Colors """
    
    def _loop_btn_color(self):
        if self._clip == None:
            return 0
        if self._clip.looping:
            return 8
        else:
            return 2

    def _play_btn_color(self):
        if self._clip == None:
            return 0
        else:
            if self._clip.is_playing:
                return 6
            else:
                if self._clip.is_triggered:
                    return 12
                else:
                    return 1
                
    def _stop_btn_color(self):
        if self._clip == None:
            return 0
        else:
            if self._clip.is_playing:
                return 11
            else:
                return 5


    
    def _btn_loop_toggl(self,v):
        if not self._clip == None and v > 0:
            if self._clip.looping:
                self._clip.looping = False
            else:
                self._clip.looping = True
            self._deck_grid[0].send_value(self._loop_btn_color())
            
    
    def _btn_step_size(self,v,b):
        self.parent.log_message("step_size")
        if v > 0:
            if self._shift:
                self._step_size = 0
            else:
                if self._step_size < 2:
                    self._step_size = self._step_size + 1
                else:
                    self._step_size = 1
            b.send_value(self._step_colors[self._step_size])
            self._deck_grid[2].send_value(self._step_colors[self._step_size])
            self._deck_grid[10].send_value(self._step_colors[self._step_size])
            self._deck_grid[3].send_value(self._step_colors[self._step_size+2])
            self._deck_grid[11].send_value(self._step_colors[self._step_size+2])
            
            
        
    def _btn_clip_play(self,v):
        if self._clip == None:
            pass
        else:
            self._clip.fire()
        
    def _btn_clip_stop(self,v):
        if not self._clip == None:
            if self._shift:
                if self._clip.looping:
                    self._clip.loop_start = 0.0
                    self._clip.loop_end = 4.0
                else:
                    self._clip.looping = True
                    self._clip.loop_start = 0.0
                    self._clip.loop_end = 4.0
                    self._clip.looping = False
            else:
                self._clip.stop()
            
            
    def _btn_dec_loop(self,v):
        if v > 0 and not self._clip == None:
            if self._shift:
                if self._clip.looping:
                    self._clip.loop_start = self._clip.loop_start - self._steps[self._step_size]
                else:
                    self._clip.looping = True
                    self._clip.loop_start = self._clip.loop_start - self._steps[self._step_size]
                    self._clip.looping = False                
            else:
                if self._clip.looping:
                    if self._clip.loop_end - self._clip.loop_start > self._steps[self._step_size]:
                        self._clip.loop_end = self._clip.loop_end - self._steps[self._step_size]
                else:
                    if self._clip.loop_end - self._clip.loop_start > self._steps[self._step_size]:
                        self._clip.looping = True
                        self._clip.loop_end = self._clip.loop_end - self._steps[self._step_size]
                        self._clip.looping = False
        
    
    def _btn_inc_loop(self,v):
        if v > 0 and not self._clip == None:
            if self._clip.looping:
                self._clip.loop_end = self._clip.loop_end + self._steps[self._step_size]
            else:
                self._clip.looping = True
                self._clip.loop_end = self._clip.loop_end + self._steps[self._step_size]
                self._clip.looping = False
    
    def _btn_mv_loop_right(self,v):
        if v > 0 and not self._clip == None:
            if self._clip.looping:
                self._clip.loop_end = self._clip.loop_end + self._steps[self._step_size]
                self._clip.loop_start = self._clip.loop_start + self._steps[self._step_size]
            else:
                self._clip.looping = True
                self._clip.loop_end = self._clip.loop_end + self._steps[self._step_size]
                self._clip.loop_start = self._clip.loop_start + self._steps[self._step_size]
                self._clip.looping = False
                
    
    def _btn_mv_loop_left(self,v):
        if v > 0 and not self._clip == None:
            if self._clip.looping:
                self._clip.loop_start = self._clip.loop_start - self._steps[self._step_size]
                self._clip.loop_end = self._clip.loop_end - self._steps[self._step_size]
            else:
                self._clip.looping = True
                self._clip.loop_start = self._clip.loop_start - self._steps[self._step_size]
                self._clip.loop_end = self._clip.loop_end - self._steps[self._step_size]
                self._clip.looping = False
    
    def _btn_zoom(self,v):
        if v > 0 and not self._clip == None:
            self.parent.song().view.highlighted_clip_slot = self._clip_slot._clip_slot
    
    def _btn_xfade(self,v):
        pass
    

    
    
    
    def _connect_deck(self):
        """ connect deck to controls """
        pass
    
    def _disconnect_deck(self):
        """ disconnect deck from controls """
        pass
    
      
        