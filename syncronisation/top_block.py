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

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import channels
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from optparse import OptionParser
import sip
import sys
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.symb_rate = symb_rate = 300
        self.samp_rate = samp_rate = 32000
        self.noise_volt = noise_volt = 0.0001
        self.filter_bw = filter_bw = 5 * symb_rate

        ##################################################
        # Blocks
        ##################################################
        self._noise_volt_range = Range(0, 1, 0.01, 0.0001, 200)
        self._noise_volt_win = RangeWidget(self._noise_volt_range, self.set_noise_volt, 'Channel: Noise Voltage', "slider", float)
        self.top_grid_layout.addWidget(self._noise_volt_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._filter_bw_range = Range(0.5 * symb_rate, 10 * symb_rate, 1, 5 * symb_rate, 200)
        self._filter_bw_win = RangeWidget(self._filter_bw_range, self.set_filter_bw, "filter_bw", "counter_slider", float)
        self.top_grid_layout.addWidget(self._filter_bw_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	3 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(3):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, filter_bw, filter_bw / 2, firdes.WIN_RECTANGULAR, 6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(1, firdes.low_pass(
        	1, samp_rate, filter_bw, filter_bw / 2, firdes.WIN_RECTANGULAR, 6.76))
        self.dc_blocker_xx_0 = filter.dc_blocker_ff(320, True)
        self.channels_channel_model_0_0 = channels.channel_model(
        	noise_voltage=noise_volt,
        	frequency_offset=0.0005,
        	epsilon=1.0,
        	taps=(1.0, ),
        	noise_seed=0,
        	block_tags=False
        )
        self.blocks_vector_source_x_0 = blocks.vector_source_f((1, 1, -1, 1, -1, -1), True, 1, [])
        self.blocks_vco_c_0 = blocks.vco_c(samp_rate, samp_rate, 1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_float*1, samp_rate / symb_rate)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((-0.5, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_mag_0_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_complex_to_arg_0 = blocks.complex_to_arg(1)
        self.analog_pll_freqdet_cf_0 = analog.pll_freqdet_cf(0.01, 0.06, -0.06)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_pll_freqdet_cf_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_complex_to_arg_0, 0), (self.dc_blocker_xx_0, 0))
        self.connect((self.blocks_complex_to_mag_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_mag_0_0, 0), (self.qtgui_time_sink_x_0, 2))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_vco_c_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.analog_pll_freqdet_cf_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_arg_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_mag_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_vco_c_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.blocks_complex_to_mag_0_0, 0))
        self.connect((self.channels_channel_model_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.dc_blocker_xx_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.channels_channel_model_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_multiply_xx_1, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_filter_bw(5 * self.symb_rate)
        self.blocks_repeat_0.set_interpolation(self.samp_rate / self.symb_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filter_bw, self.filter_bw / 2, firdes.WIN_RECTANGULAR, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filter_bw, self.filter_bw / 2, firdes.WIN_RECTANGULAR, 6.76))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.blocks_repeat_0.set_interpolation(self.samp_rate / self.symb_rate)

    def get_noise_volt(self):
        return self.noise_volt

    def set_noise_volt(self, noise_volt):
        self.noise_volt = noise_volt
        self.channels_channel_model_0_0.set_noise_voltage(self.noise_volt)

    def get_filter_bw(self):
        return self.filter_bw

    def set_filter_bw(self, filter_bw):
        self.filter_bw = filter_bw
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filter_bw, self.filter_bw / 2, firdes.WIN_RECTANGULAR, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.filter_bw, self.filter_bw / 2, firdes.WIN_RECTANGULAR, 6.76))


def main(top_block_cls=top_block, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
