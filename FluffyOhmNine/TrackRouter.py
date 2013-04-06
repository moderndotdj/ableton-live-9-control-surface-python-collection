'''
Created on Jan 4, 2013

@author: simonfuog
'''

""" Track Strings """
FLK_DECK = ["1. Deck","2. Deck","3. Deck","4. Deck"]


class TrackRouter(object):
    '''
    handles the routing from clip tracks to deck tracks.
    when route-btn is presst:
    1. check if targed is closed
    2. remove all routings to target
    3. set output of selected clip track to deck-string
    
    '''


    def __init__(self,p):
        '''
        Constructor
        '''
        self.parent = p
        self._clip_tracks = [];
        self._deck_tracks = [None,None,None,None]
        self._btns = [None,None,None,None]
        self._initial = True
    
    def set_router_buttons(self, btns):
        if btns[0] == None and btns[1] == None and btns[2] == None and btns[3] == None:
            for b in self._btns:
                b.remove_value_listener(self._btn_press)
        else:
            self._btns = btns
            for cnt in range(4):
                self._btns[cnt].r = cnt
                self._btns[cnt].add_value_listener(self._btn_press,True)
                self._set_rt_btn_color(cnt)
            if self._initial:
                self._initial=False
                self.setup_clip_tracks()
        
    def _btn_press(self,v,b):
        """ when rt-btn is pressed """
        if v > 0:
            src = self._clip_tracks[0]
            for tr in self._clip_tracks:
                if tr.is_part_of_selection:
                    src = tr
                    #self.parent.log_message(tr.name)
            self._route_to_deck(src, b.r)
            self._set_rt_btn_color(b.r)
    
    def update_color(self):
        for x in range(4):
            self._set_rt_btn_color(x)
        
    def _set_rt_btn_color(self,x):
        if self._is_routable_target(self._deck_tracks[x]):
            self._btns[x].send_value(4)
        else:
            self._btns[x].send_value(5)

    def set_target_tracks(self, tr1, tr2, tr3, tr4):
        self._deck_tracks[0] = tr1
        self._deck_tracks[1] = tr2
        self._deck_tracks[2] = tr3
        self._deck_tracks[3] = tr4
    
    def setup_clip_tracks(self):
        for tr in self._clip_tracks:
            #self.parent.log_message("reset track output for: " + tr.current_output_routing)
            x = u'Sends Only'
            #x = tr.current_output_routing
            #self.parent.log_message("eq: " + `type(tr)`)
            tr.current_output_routing = x

    def add_clip_track(self,tr):
        self._clip_tracks.append(tr)

    def _route_to_deck(self,clip_track,deck_track_nr):
        deck_track = self._deck_tracks[deck_track_nr]
        if self._is_routable(deck_track,clip_track):
            #self.parent.log_message("eqqqqqqqqqqqqq ")
            self._remove_from_deck(deck_track.name)
            clip_track.current_output_routing = deck_track.name
            self._update_deck_clip(deck_track_nr, clip_track)
        
        
    def _is_routable(self,deck_tr,clip_tr):
        if self._is_routable_source(clip_tr) and self._is_routable_target(deck_tr):
            return True
        else:
            return False
        
    def _is_routable_source(self,tr):
        if tr.current_output_routing == "Sends Only":
            return True
        else:
            return False   


    def _is_routable_target(self,tr):
        if tr.mixer_device.volume.value == 0.0:
            return True
        else:
            return False
    
    def _remove_from_deck(self,deck_string):
        for tr in self._clip_tracks:
            if tr.current_output_routing == deck_string:
                tr.current_output_routing = "Sends Only"


        
    def _update_deck_clip(self,deck_nr, clip_track = None):
        if clip_track == None:
            clip_track = self.parent._trackdecks[deck_nr]._current_clip_track
            
        if not clip_track == None:
            slt = None
            sltt = None
            for cs in clip_track.clip_slots:
                if cs.is_playing:
                    slt = cs
                if cs.is_triggered:
                    sltt = cs
            if sltt == None:
                sltt = slt
                    
            self.parent._trackdecks[deck_nr].set_clip(sltt,clip_track)
                    
                    
                    
                    