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

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
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
        self.freq_tune = freq_tune = 0
        self.band_select = band_select = 95e6
        self.transm_freq = transm_freq = band_select + freq_tune
        self.samp_rate = samp_rate = 44000
        self.rf_samp_rate = rf_samp_rate = 2400000
        self.rf_gain = rf_gain = False

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
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=transm_freq,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=rf_samp_rate,
        	fft_size=1024,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=rf_samp_rate,
                decimation=2*samp_rate,
                taps=None,
                fractional_bw=0.4,
        )
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + 'hackrf=2e12c3' )
        self.osmosdr_sink_0.set_sample_rate(rf_samp_rate)
        self.osmosdr_sink_0.set_center_freq(transm_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(0, 0)
        self.osmosdr_sink_0.set_gain(rf_gain, 0)
        self.osmosdr_sink_0.set_if_gain(20, 0)
        self.osmosdr_sink_0.set_bb_gain(20, 0)
        self.osmosdr_sink_0.set_antenna('', 0)
        self.osmosdr_sink_0.set_bandwidth(0, 0)

        _freq_tune_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_tune_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_tune_sizer,
        	value=self.freq_tune,
        	callback=self.set_freq_tune,
        	label='FREQ',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_tune_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_tune_sizer,
        	value=self.freq_tune,
        	callback=self.set_freq_tune,
        	minimum=-10e6,
        	maximum=10e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_tune_sizer)
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\andro\\Downloads\\9bb7baf38e7564.wav', True)
        self._band_select_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.band_select,
        	callback=self.set_band_select,
        	label='BAND',
        	choices=[95e6, 130e6, 433e6],
        	labels=[],
        )
        self.Add(self._band_select_chooser)
        self.analog_wfm_tx_0 = analog.wfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=2*samp_rate,
        	tau=75e-6,
        	max_dev=75e3,
        	fh=-1.0,
        )



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_wfm_tx_0, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.analog_wfm_tx_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.osmosdr_sink_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.wxgui_fftsink2_0, 0))

    def get_freq_tune(self):
        return self.freq_tune

    def set_freq_tune(self, freq_tune):
        self.freq_tune = freq_tune
        self.set_transm_freq(self.band_select + self.freq_tune)
        self._freq_tune_slider.set_value(self.freq_tune)
        self._freq_tune_text_box.set_value(self.freq_tune)

    def get_band_select(self):
        return self.band_select

    def set_band_select(self, band_select):
        self.band_select = band_select
        self.set_transm_freq(self.band_select + self.freq_tune)
        self._band_select_chooser.set_value(self.band_select)

    def get_transm_freq(self):
        return self.transm_freq

    def set_transm_freq(self, transm_freq):
        self.transm_freq = transm_freq
        self.wxgui_fftsink2_0.set_baseband_freq(self.transm_freq)
        self.osmosdr_sink_0.set_center_freq(self.transm_freq, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate
        self.wxgui_fftsink2_0.set_sample_rate(self.rf_samp_rate)
        self.osmosdr_sink_0.set_sample_rate(self.rf_samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_check_box.set_value(self.rf_gain)
        self.osmosdr_sink_0.set_gain(self.rf_gain, 0)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
