from _Framework.ChannelStripComponent import ChannelStripComponent

class LividChanStripComponent(ChannelStripComponent):
  ' Customized chan strip which limits volume to 0db '

  def _select_value(self, value):
    was_selected = (self.song().view.selected_track == self._track)
    ChannelStripComponent._select_value(self, value)

    if was_selected and self.is_enabled() and (self._track != None):
      if (value >= 1):
        if self.application().view.is_view_visible('Detail/Clip'):
          self.application().view.show_view('Detail/DeviceChain')
          self.application().view.is_view_visible('Detail/DeviceChain')
        else:
          self.application().view.show_view('Detail/Clip')
          self.application().view.is_view_visible('Detail/Clip')

          # Select playing clip when detail view is shown
          if self._track.playing_slot_index >= 0:
            playing_clip = self._track.clip_slots[self._track.playing_slot_index].clip
            self.song().view.detail_clip = playing_clip
