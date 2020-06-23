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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from bfsk_rcv import bfsk_rcv  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.wxgui import forms
from gnuradio.wxgui import numbersink2
from gnuradio.wxgui import scopesink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import math
import wx


class top_block(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Top Block")
        _icon_path = "C:\Program Files\GNURadio-3.7\share\icons\hicolor\scalable/apps\gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.noise_volt_db = noise_volt_db = -30
        self.symb_rate = symb_rate = 10000
        self.samp_rate = samp_rate = 100000
        self.pi = pi = 3.14152
        self.noise_volt = noise_volt = math.pow(10, noise_volt_db / 20)
        self.freq_offset = freq_offset = 0
        self.error_count_decim = error_count_decim = 100000.0
        self.delay = delay = 2

        ##################################################
        # Blocks
        ##################################################
        _freq_offset_sizer = wx.BoxSizer(wx.VERTICAL)
        self._freq_offset_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_freq_offset_sizer,
        	value=self.freq_offset,
        	callback=self.set_freq_offset,
        	label='freq_offset',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._freq_offset_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_freq_offset_sizer,
        	value=self.freq_offset,
        	callback=self.set_freq_offset,
        	minimum=0,
        	maximum=0.01,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_freq_offset_sizer)
        _delay_sizer = wx.BoxSizer(wx.VERTICAL)
        self._delay_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_delay_sizer,
        	value=self.delay,
        	callback=self.set_delay,
        	label='delay',
        	converter=forms.int_converter(),
        	proportion=0,
        )
        self._delay_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_delay_sizer,
        	value=self.delay,
        	callback=self.set_delay,
        	minimum=0,
        	maximum=100,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=int,
        	proportion=1,
        )
        self.Add(_delay_sizer)
        self.wxgui_scopesink2_2 = scopesink2.scope_sink_f(
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
        self.Add(self.wxgui_scopesink2_2.win)
        self.wxgui_numbersink2_0 = numbersink2.number_sink_f(
        	self.GetWin(),
        	unit='',
        	minval=0,
        	maxval=0.4,
        	factor=1 / error_count_decim,
        	decimal_places=10,
        	ref_level=0,
        	sample_rate=symb_rate / error_count_decim,
        	number_rate=1,
        	average=False,
        	avg_alpha=None,
        	label='Bit Error Probability',
        	peak_hold=False,
        	show_gauge=True,
        )
        self.Add(self.wxgui_numbersink2_0.win)
        _noise_volt_db_sizer = wx.BoxSizer(wx.VERTICAL)
        self._noise_volt_db_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_noise_volt_db_sizer,
        	value=self.noise_volt_db,
        	callback=self.set_noise_volt_db,
        	label='noise_volt_db',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._noise_volt_db_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_noise_volt_db_sizer,
        	value=self.noise_volt_db,
        	callback=self.set_noise_volt_db,
        	minimum=-30,
        	maximum=5,
        	num_steps=35,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_noise_volt_db_sizer)
        self.channels_channel_model_0_0 = channels.channel_model(
        	noise_voltage=noise_volt,
        	frequency_offset=freq_offset,
        	epsilon=1.0,
        	taps=(1.0, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_vector_source_x_0_0 = blocks.vector_source_f((-1, 1, 1, 1, 1, 1), True, 1, [])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, samp_rate / symb_rate)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((0.5, ))
        self.blocks_integrate_xx_0 = blocks.integrate_ff(int(error_count_decim), 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, delay)
        self.blocks_copy_0 = blocks.copy(gr.sizeof_float*1)
        self.blocks_copy_0.set_enabled(True)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vff((1, ))
        self.blocks_abs_xx_0 = blocks.abs_ff(1)
        self.bfsk_rcv_0 = bfsk_rcv(
            samp_rate=samp_rate,
            symb_rate=symb_rate,
        )
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*pi*float(symb_rate)/float(samp_rate))



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.bfsk_rcv_0, 3), (self.blocks_char_to_float_1, 0))
        self.connect((self.blocks_abs_xx_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_abs_xx_0, 0), (self.wxgui_scopesink2_2, 0))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_char_to_float_1, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.blocks_copy_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_copy_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.wxgui_numbersink2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.analog_frequency_modulator_fc_0, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_abs_xx_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.channels_channel_model_0_0, 0))
        self.connect((self.blocks_vector_source_x_0_0, 0), (self.blocks_copy_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.bfsk_rcv_0, 0))

    def get_noise_volt_db(self):
        return self.noise_volt_db

    def set_noise_volt_db(self, noise_volt_db):
        self.noise_volt_db = noise_volt_db
        self.set_noise_volt(math.pow(10, self.noise_volt_db / 20) )
        self._noise_volt_db_slider.set_value(self.noise_volt_db)
        self._noise_volt_db_text_box.set_value(self.noise_volt_db)

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.blocks_repeat_0.set_interpolation(self.samp_rate / self.symb_rate)
        self.bfsk_rcv_0.set_symb_rate(self.symb_rate)
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*self.pi*float(self.symb_rate)/float(self.samp_rate))

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.wxgui_scopesink2_2.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_repeat_0.set_interpolation(self.samp_rate / self.symb_rate)
        self.bfsk_rcv_0.set_samp_rate(self.samp_rate)
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*self.pi*float(self.symb_rate)/float(self.samp_rate))

    def get_pi(self):
        return self.pi

    def set_pi(self, pi):
        self.pi = pi
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*self.pi*float(self.symb_rate)/float(self.samp_rate))

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0_0.set_noise_voltage(self.noise_volt)

    def get_freq_offset(self):
        return self.freq_offset

    def set_freq_offset(self, freq_offset):
        self.freq_offset = freq_offset
        self._freq_offset_slider.set_value(self.freq_offset)
        self._freq_offset_text_box.set_value(self.freq_offset)
        self.channels_channel_model_0_0.set_frequency_offset(self.freq_offset)

    def get_error_count_decim(self):
        return self.error_count_decim

    def set_error_count_decim(self, error_count_decim):
        self.error_count_decim = error_count_decim

    def get_delay(self):
        return self.delay

    def set_delay(self, delay):
        self.delay = delay
        self._delay_slider.set_value(self.delay)
        self._delay_text_box.set_value(self.delay)
        self.blocks_delay_0.set_dly(self.delay)


def main(top_block_cls=top_block, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
