#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# GNU Radio version: 3.7.13.5
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import epy_block_0
import osmosdr
import time
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000
        self.rf_samp_rate = rf_samp_rate = 2048000
        self.rf_gain = rf_gain = 0
        self.freq = freq = 434040000
        self.base = base = 0x9F78B0
        self.D = D = 0
        self.C = C = 0
        self.B = B = 0
        self.A = A = 0

        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_check_box = forms.check_box(
        	parent=self.GetWin(),
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label='rf_gain',
        	true=14,
        	false=0,
        )
        self.Add(self._rf_gain_check_box)
        self._freq_text_box = forms.text_box(
        	parent=self.GetWin(),
        	value=self.freq,
        	callback=self.set_freq,
        	label='Freq',
        	converter=forms.float_converter(),
        )
        self.Add(self._freq_text_box)
        self._D_check_box = forms.check_box(
        	parent=self.GetWin(),
        	value=self.D,
        	callback=self.set_D,
        	label='D',
        	true=8,
        	false=0,
        )
        self.Add(self._D_check_box)
        self._C_check_box = forms.check_box(
        	parent=self.GetWin(),
        	value=self.C,
        	callback=self.set_C,
        	label='C',
        	true=4,
        	false=0,
        )
        self.Add(self._C_check_box)
        self._B_check_box = forms.check_box(
        	parent=self.GetWin(),
        	value=self.B,
        	callback=self.set_B,
        	label='B',
        	true=2,
        	false=0,
        )
        self.Add(self._B_check_box)
        self._A_check_box = forms.check_box(
        	parent=self.GetWin(),
        	value=self.A,
        	callback=self.set_A,
        	label='A',
        	true=1,
        	false=0,
        )
        self.Add(self._A_check_box)
        self.wxgui_scopesink2_0 = scopesink2.scope_sink_c(
        	self.GetWin(),
        	title='Scope Plot',
        	sample_rate=samp_rate,
        	v_scale=0,
        	v_offset=0,
        	t_scale=0,
        	ac_couple=False,
        	xy_mode=False,
        	num_inputs=1,
        	trig_mode=wxgui.TRIG_MODE_AUTO,
        	y_axis_label='Counts',
        )
        self.Add(self.wxgui_scopesink2_0.win)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=rf_samp_rate,
                decimation=samp_rate,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'hackrf=2e12c3,buffers=2' )
        self.osmosdr_sink_0.set_sample_rate(rf_samp_rate)
        self.osmosdr_sink_0.set_center_freq(freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        self.epy_block_0 = epy_block_0.blk(sample_rate=samp_rate, short_impulse_len=0.0003, long_impulse_len=0.0011, packet_separator_len=0.005, packet_len=24, data=A + B + C + D + base)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.epy_block_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.epy_block_0, 0), (self.wxgui_scopesink2_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.osmosdr_sink_0, 0))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_0.set_sample_rate(self.samp_rate)
        self.epy_block_0.sample_rate = self.samp_rate

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate
        self.osmosdr_sink_0.set_sample_rate(self.rf_samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_check_box.set_value(self.rf_gain)
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self._freq_text_box.set_value(self.freq)
        self.osmosdr_sink_0.set_center_freq(self.freq, 0)

    def get_base(self):
        return self.base

    def set_base(self, base):
        self.base = base
        self.epy_block_0.data = self.A + self.B + self.C + self.D + self.base

    def get_D(self):
        return self.D

    def set_D(self, D):
        self.D = D
        self._D_check_box.set_value(self.D)
        self.epy_block_0.data = self.A + self.B + self.C + self.D + self.base

    def get_C(self):
        return self.C

    def set_C(self, C):
        self.C = C
        self._C_check_box.set_value(self.C)
        self.epy_block_0.data = self.A + self.B + self.C + self.D + self.base

    def get_B(self):
        return self.B

    def set_B(self, B):
        self.B = B
        self._B_check_box.set_value(self.B)
        self.epy_block_0.data = self.A + self.B + self.C + self.D + self.base

    def get_A(self):
        return self.A

    def set_A(self, A):
        self.A = A
        self._A_check_box.set_value(self.A)
        self.epy_block_0.data = self.A + self.B + self.C + self.D + self.base


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
