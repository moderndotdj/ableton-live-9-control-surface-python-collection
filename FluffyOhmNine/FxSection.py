'''
Created on Jan 11, 2013

@author: simonfuog
'''

        

class FxStrip(object):
    """ represents one fader/enc/btn of the OhmRGBs right mixer section """
    
    def __init__(self,p,t,f,e,b,nr):
        self._parent = p
        self._fader = f
        self._encoder = e
        self._btn = b
        self._reset_btn = None
        self._track = t
        self._nr = nr
        
        self._deck_btns = None
        
        self._fxs = [None,None,None,None,None,None]
        self._current_fx = None
    
        self._load_fxs()
    
    
    def _load_fxs(self):
        for d in self._track.devices:
            if d.name == "CrossComp":
                self._fxs[4] = CrossCompFx(self,4,d)
            elif d.name == "EQ3":
                self._fxs[5] = EQFx(self,5,d)
            elif d.name == "Fx1":
                self._fxs[0] = Fx(self,0,d)
            elif d.name == "Fx2":
                self._fxs[1] = Fx(self,1,d)
            elif d.name == "Fx3":
                self._fxs[2] = Fx(self,2,d)
            elif d.name == "Fx4":
                self._fxs[3] = Fx(self,3,d)
            
                
    
    def set_btns(self,b):
        if b == None:
            for bt in self._deck_btns:
                bt.remove_value_listener(self._fx_btn_values)
            self._deck_btns = None
            for f in self._fxs:
                if f != None:
                    f.detouch(True)
                    f._btn = None
            
            self._reset_btn = None
            
            
        else:
            for i in range(6):
                if i > 4:
                    b[i].fx = 99
                    self._reset_btn = b[i]
                    self._set_reset_all_color()
                else:
                    b[i].fx = self._nr * 10 + i
                    if self._fxs[i] != None:
                        self._fxs[i].set_btn(b[i])
                b[i].add_value_listener(self._fx_btn_values,True)
            self._deck_btns = b
        
        
    def _fx_btn_values(self,v,b):
        if v > 0:
            if b.fx == 99: # reset
                self._reset_all_fx()
            elif self._current_fx == None:
                    self.setup_fx(b.fx - self._nr * 10)
            elif b.fx == self._nr * 10 + self._current_fx._nr: # pressd current fx btn
                self._current_fx.turn_on_q()
            else:
                if self._parent.parent.shifted:
                    if self._fxs[b.fx - self._nr * 10] != None:
                        self._fxs[b.fx - self._nr * 10].turn_on()
                else:
                    self.setup_fx(b.fx - self._nr * 10)
                
                
    def setup_fx(self,fx_nr):
        if self._current_fx != None:
            self._current_fx.detouch()
        if self._fxs[fx_nr] != None:
            self._current_fx = self._fxs[fx_nr]
            if self._current_fx._btn != None:
                self._current_fx._btn.send_value(self._current_fx._get_color())
                self._current_fx.attach()
        
    def _set_reset_all_color(self):
        self._reset_btn.send_value(5)
        
        
    def _reset_all_fx(self):
        for f in self._fxs:
            if f != None:
                f.reset()
            
            
    
class Fx(object):
    """ super of all fxs """
    def __init__(self,p,nr,dev):
        self._parent = p
        self._device = dev
        self._btn = None
        self._nr = nr
        self._touched = False
        
        self._default_evalue = 127
        self._default_fvalue = 127
        
        self._fader_pickedup = False
        self._encoder_pickedup = False
        
        self.log("Initialized")
        
    
    def turn_on(self):
        self.log("turn on")
        self._touched = True
        self._device.parameters[1].value = self._default_fvalue
        self._device.parameters[2].value = self._default_evalue
        self._fader_pickedup = False
        self._encoder_pickedup = False
        if self._btn != None:
            self._btn.send_value(self._get_color())
        self._set_reset_color()
    
    def turn_on_q(self): # quantized
        self.turn_on()
    
    def set_btn(self,b):
        self._btn = b
        if self._device.parameters[1].value > self._device.parameters[1].min or self._device.parameters[2].value > self._device.parameters[2].min:
            self._touched = True
        b.send_value(self._get_color())
        self._set_reset_color()
     
    def attach(self):
        if self._nr < 5:
            self._parent._btn.add_value_listener(self._btn_value,False)
            self._parent._fader.add_value_listener(self._fader_value,False)
            self._parent._encoder.add_value_listener(self._enc_value,False)
            self._set_reset_color()
        
        
    def _btn_value(self,v):
        if v > 0:
            if self._parent._parent.parent.shifted:
                self._default_fvalue = self._device.parameters[1].value
                self._default_evalue = self._device.parameters[2].value
            else:
                self.reset()
                
        self.log(`v`)   
    def _fader_value(self,v):
        par = self._device.parameters[1]
        val = v * par.max / 127
        if v < 4 and par.value == par.min:
            self._fader_pickedup = True
        if not self._fader_pickedup:
            if par.value + 2 < val:
                pass
            elif par.value - 2 > val:
                pass
            else:
                self._fader_pickedup = True
        else:
            par.value = val
            if not self._touched and v > 0:
                self._touched = True
                if self._btn != None:
                    self._btn.send_value(self._get_color())
                self._set_reset_color()
            
        #self.log(`val`)
        #self.log(`par.max`)
        #self.log(`par.min`)
        #self.log(`par.value`)    
    def _enc_value(self,v):
        par = self._device.parameters[2]
        val = v * par.max / 127
        if v < 4 and par.value == par.min:
            self._encoder_pickedup = True
        if not self._encoder_pickedup:
            if par.value + 2 < val:
                pass
            elif par.value - 2 > val:
                pass
            else:
                self._encoder_pickedup = True
        else:
            par.value = val
            if not self._touched and v > 0:
                self._touched = True
                if self._btn != None:
                    self._btn.send_value(self._get_color())
                self._set_reset_color()
        #self.log(`v`)   
        
    def _get_color(self):
        col = 1
        if self._parent._current_fx == self:
            col = col + 1
        if self._touched:
            col = col + 12
        
            
        return col
    
    
    def _set_reset_color(self):
        col = 0
        if self._parent._current_fx == self:
            col = col + 5
            if self._touched:
                col = col + 12
        self._parent._btn.send_value(col)
    
    def detouch(self,page_switch=False):
        if self._btn != None:
            if not page_switch:
                if self._parent._current_fx == self:
                    self._parent._btn.remove_value_listener(self._btn_value)
                    self._parent._fader.remove_value_listener(self._fader_value)
                    self._parent._encoder.remove_value_listener(self._enc_value)
                    self._fader_pickedup = False
                    self._parent._current_fx = None
                self._btn.send_value(self._get_color())
            self._set_reset_color()
        self.log(`self._get_color()`)
        self.log("de-touch")
    
    def reset(self):
        self.log("reset")
        self._touched = False
        self._fader_pickedup = False
        self._encoder_pickedup = False
        if self._btn != None:
            self._btn.send_value(self._get_color())
            self._device.parameters[1].value = self._device.parameters[1].min
            self._device.parameters[2].value = self._device.parameters[2].min
        self._set_reset_color()
    
    def log(self,s):
        self._parent._parent.parent.log_message("Fx" + `self._nr` + ":" + s)

class CrossCompFx(Fx):
    
    def __init__(self,p,nr,dev):
        Fx.__init__(self, p, nr, dev)
        
    def _get_color(self):
        col = 1
        if self._parent._current_fx == self:
            col = col + 1
        if self._touched:
            col = col + 12
            self._parent._parent.set_cross_signal(True)
        else:
            self._parent._parent.set_cross_signal(False)
        return col
        

class EQFx(Fx):
    
    def __init__(self,p,nr,dev):
        Fx.__init__(self, p, nr, dev)
        
        self._pickedup_hi = False
        self._pickedup_mi = False
        self._pickedup_lo = False
        
        self._enc_hi = p._parent.parent._enc[0+p._nr]
        self._enc_mi = p._parent.parent._enc[4+p._nr]
        self._enc_lo = p._parent.parent._enc[8+p._nr]
        
        self._enc_hi.add_value_listener(self._enc_hi_value,False)
        self._enc_mi.add_value_listener(self._enc_mi_value,False)
        self._enc_lo.add_value_listener(self._enc_lo_value,False)
        
            
    def _enc_hi_value(self,v):
        par = self._device.parameters[3]
        val = v * par.max / 127
        if v < 4 and par.value == par.min:
            self._pickedup_hi = True
        if not self._pickedup_hi:
            if par.value + 2 < val:
                pass
            elif par.value - 2 > val:
                pass
            else:
                self._pickedup_hi = True
        else:
            par.value = val
            if not self._touched and v > 0:
                self._touched = True
                            
    def _enc_mi_value(self,v):
        par = self._device.parameters[2]
        val = v * par.max / 127
        if v < 4 and par.value == par.min:
            self._pickedup_mi = True
        if not self._pickedup_mi:
            if par.value + 2 < val:
                pass
            elif par.value - 2 > val:
                pass
            else:
                self._pickedup_mi = True
        else:
            par.value = val
            if not self._touched and v > 0:
                self._touched = True
                            
    def _enc_lo_value(self,v):
        par = self._device.parameters[1]
        val = v * par.max / 127
        if v < 4 and par.value == par.min:
            self._pickedup_lo = True
        if not self._pickedup_lo:
            if par.value + 2 < val:
                pass
            elif par.value - 2 > val:
                pass
            else:
                self._pickedup_lo = True
        else:
            par.value = val
            if not self._touched and v > 0:
                self._touched = True
                
    
    def reset(self):
        self.log("reset")
        self._touched = False
        self._pickedup_hi = False
        self._pickedup_mi = False
        self._pickedup_lo = False
            
        self._device.parameters[1].value = self._device.parameters[1].max
        self._device.parameters[2].value = self._device.parameters[2].max
        self._device.parameters[3].value = self._device.parameters[3].max
        self._set_reset_color()




