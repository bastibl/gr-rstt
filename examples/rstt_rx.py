#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: RSTT - frame recorder
# Description: Decode transmission from radiosonde and store frames in file on disc
# GNU Radio version: 3.8tech-preview-381-g27dd99e4

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from datetime import datetime
from gnuradio import analog
import math
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio import gr
import sys
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
import rstt
import time
from gnuradio import qtgui

class rstt_rx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "RSTT - frame recorder")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("RSTT - frame recorder")
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

        self.settings = Qt.QSettings("GNU Radio", "rstt_rx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.symb_rate = symb_rate = 4800
        self.oversample = oversample = 2
        self.freq_tune = freq_tune = 2669000
        self.dec_xlate = dec_xlate = 1
        self.dec_low_pass = dec_low_pass = 240
        self.samp_rate = samp_rate = symb_rate*oversample*dec_xlate*dec_low_pass
        self.rf_gain_auto = rf_gain_auto = True
        self.rf_gain = rf_gain = 20
        self.freq_ppm = freq_ppm = 0
        self.freq_offs = freq_offs = -750000
        self.freq = freq = 400000000+freq_tune
        self.enable_tune_ppm_checkbox = enable_tune_ppm_checkbox = False
        self.dec_tune = dec_tune = 30

        ##################################################
        # Blocks
        ##################################################
        self.tabs = Qt.QTabWidget()
        self.tabs_widget_0 = Qt.QWidget()
        self.tabs_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_0)
        self.tabs_grid_layout_0 = Qt.QGridLayout()
        self.tabs_layout_0.addLayout(self.tabs_grid_layout_0)
        self.tabs.addTab(self.tabs_widget_0, 'Channel')
        self.tabs_widget_1 = Qt.QWidget()
        self.tabs_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_1)
        self.tabs_grid_layout_1 = Qt.QGridLayout()
        self.tabs_layout_1.addLayout(self.tabs_grid_layout_1)
        self.tabs.addTab(self.tabs_widget_1, 'Baseband')
        self.tabs_widget_2 = Qt.QWidget()
        self.tabs_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_2)
        self.tabs_grid_layout_2 = Qt.QGridLayout()
        self.tabs_layout_2.addLayout(self.tabs_grid_layout_2)
        self.tabs.addTab(self.tabs_widget_2, 'Number')
        self.tabs_widget_3 = Qt.QWidget()
        self.tabs_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.tabs_widget_3)
        self.tabs_grid_layout_3 = Qt.QGridLayout()
        self.tabs_layout_3.addLayout(self.tabs_grid_layout_3)
        self.tabs.addTab(self.tabs_widget_3, 'Config')
        self.top_grid_layout.addWidget(self.tabs)
        self.rstt_panel_0 = rstt.rsttPanel()
        self._rstt_panel_0_win = self.rstt_panel_0
        self.top_grid_layout.addWidget(self._rstt_panel_0_win)
        self.rstt_decoder_0 = rstt.decoder(20*10, 32, True)
        _rf_gain_auto_check_box = Qt.QCheckBox('rf_gain_auto')
        self._rf_gain_auto_choices = {True: True, False: False}
        self._rf_gain_auto_choices_inv = dict((v,k) for k,v in self._rf_gain_auto_choices.items())
        self._rf_gain_auto_callback = lambda i: Qt.QMetaObject.invokeMethod(_rf_gain_auto_check_box, "setChecked", Qt.Q_ARG("bool", self._rf_gain_auto_choices_inv[i]))
        self._rf_gain_auto_callback(self.rf_gain_auto)
        _rf_gain_auto_check_box.stateChanged.connect(lambda i: self.set_rf_gain_auto(self._rf_gain_auto_choices[bool(i)]))
        self.tabs_layout_3.addWidget(_rf_gain_auto_check_box)
        self._rf_gain_range = Range(-40, 160, 1, 20, 200)
        self._rf_gain_win = RangeWidget(self._rf_gain_range, self.set_rf_gain, 'rf_gain', "counter_slider", float)
        self.tabs_layout_3.addWidget(self._rf_gain_win)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.tabs_layout_2.addWidget(self._qtgui_number_sink_0_win)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate/dec_xlate/dec_low_pass, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.tabs_layout_0.addWidget(self._qtgui_freq_sink_x_0_0_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            firdes.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate/dec_xlate, #bw
            "", #name
            1
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)



        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.tabs_layout_1.addWidget(self._qtgui_freq_sink_x_0_win)
        self.pfb_decimator_ccf_0 = pfb.decimator_ccf(
            15,
            [1],
            0,
            100,
            True,
            True)
        self.pfb_decimator_ccf_0.declare_sample_delay(0)
        self.low_pass_filter_0_0 = filter.fir_filter_ccf(
            6,
            firdes.low_pass(
                1,
                samp_rate/dec_xlate,
                95000,
                10000,
                firdes.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            dec_low_pass,
            firdes.low_pass(
                1,
                samp_rate/dec_xlate,
                5400,
                450,
                firdes.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(dec_xlate, [1], 0, samp_rate)
        self._freq_tune_range = Range(0, 4000000, 1000, 2669000, 200)
        self._freq_tune_win = RangeWidget(self._freq_tune_range, self.set_freq_tune, 'freq_tune', "counter_slider", float)
        self.top_grid_layout.addWidget(self._freq_tune_win)
        self._freq_ppm_range = Range(-200, 200, 1, 0, 200)
        self._freq_ppm_win = RangeWidget(self._freq_ppm_range, self.set_freq_ppm, 'freq_ppm', "counter_slider", float)
        self.tabs_layout_3.addWidget(self._freq_ppm_win)
        self.freq_err_probe = blocks.probe_signal_f()
        _enable_tune_ppm_checkbox_check_box = Qt.QCheckBox('enable_tune_ppm_checkbox')
        self._enable_tune_ppm_checkbox_choices = {True: 1, False: 0}
        self._enable_tune_ppm_checkbox_choices_inv = dict((v,k) for k,v in self._enable_tune_ppm_checkbox_choices.items())
        self._enable_tune_ppm_checkbox_callback = lambda i: Qt.QMetaObject.invokeMethod(_enable_tune_ppm_checkbox_check_box, "setChecked", Qt.Q_ARG("bool", self._enable_tune_ppm_checkbox_choices_inv[i]))
        self._enable_tune_ppm_checkbox_callback(self.enable_tune_ppm_checkbox)
        _enable_tune_ppm_checkbox_check_box.stateChanged.connect(lambda i: self.set_enable_tune_ppm_checkbox(self._enable_tune_ppm_checkbox_choices[bool(i)]))
        self.tabs_layout_3.addWidget(_enable_tune_ppm_checkbox_check_box)
        self.digital_gmsk_demod_0 = digital.gmsk_demod(
            samples_per_symbol=oversample,
            gain_mu=0.1,
            mu=0.5,
            omega_relative_limit=0.005,
            freq_error=0.0,
            verbose=False,log=False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(0.05)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(int(samp_rate/dec_xlate/dec_tune), 1)
        self.analog_quadrature_demod_cf_0 = analog.quadrature_demod_cf(samp_rate/dec_xlate/dec_tune/(2*math.pi*4800))
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.analog_quadrature_demod_cf_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.freq_err_probe, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.digital_gmsk_demod_0, 0), (self.rstt_decoder_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.pfb_decimator_ccf_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.digital_gmsk_demod_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.low_pass_filter_0_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.pfb_decimator_ccf_0, 0), (self.analog_quadrature_demod_cf_0, 0))
        self.connect((self.rstt_decoder_0, 0), (self.rstt_panel_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "rstt_rx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_symb_rate(self):
        return self.symb_rate

    def set_symb_rate(self, symb_rate):
        self.symb_rate = symb_rate
        self.set_samp_rate(self.symb_rate*self.oversample*self.dec_xlate*self.dec_low_pass)

    def get_oversample(self):
        return self.oversample

    def set_oversample(self, oversample):
        self.oversample = oversample
        self.set_samp_rate(self.symb_rate*self.oversample*self.dec_xlate*self.dec_low_pass)

    def get_freq_tune(self):
        return self.freq_tune

    def set_freq_tune(self, freq_tune):
        self.freq_tune = freq_tune
        self.set_freq(400000000+self.freq_tune)

    def get_dec_xlate(self):
        return self.dec_xlate

    def set_dec_xlate(self, dec_xlate):
        self.dec_xlate = dec_xlate
        self.set_samp_rate(self.symb_rate*self.oversample*self.dec_xlate*self.dec_low_pass)
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/self.dec_xlate/self.dec_tune/(2*math.pi*4800))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.dec_xlate, 5400, 450, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate/self.dec_xlate, 95000, 10000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate/self.dec_xlate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate/self.dec_xlate/self.dec_low_pass)

    def get_dec_low_pass(self):
        return self.dec_low_pass

    def set_dec_low_pass(self, dec_low_pass):
        self.dec_low_pass = dec_low_pass
        self.set_samp_rate(self.symb_rate*self.oversample*self.dec_xlate*self.dec_low_pass)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate/self.dec_xlate/self.dec_low_pass)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/self.dec_xlate/self.dec_tune/(2*math.pi*4800))
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate/self.dec_xlate, 5400, 450, firdes.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.samp_rate/self.dec_xlate, 95000, 10000, firdes.WIN_HAMMING, 6.76))
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate/self.dec_xlate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate/self.dec_xlate/self.dec_low_pass)

    def get_rf_gain_auto(self):
        return self.rf_gain_auto

    def set_rf_gain_auto(self, rf_gain_auto):
        self.rf_gain_auto = rf_gain_auto
        self._rf_gain_auto_callback(self.rf_gain_auto)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain

    def get_freq_ppm(self):
        return self.freq_ppm

    def set_freq_ppm(self, freq_ppm):
        self.freq_ppm = freq_ppm

    def get_freq_offs(self):
        return self.freq_offs

    def set_freq_offs(self, freq_offs):
        self.freq_offs = freq_offs

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq

    def get_enable_tune_ppm_checkbox(self):
        return self.enable_tune_ppm_checkbox

    def set_enable_tune_ppm_checkbox(self, enable_tune_ppm_checkbox):
        self.enable_tune_ppm_checkbox = enable_tune_ppm_checkbox
        self._enable_tune_ppm_checkbox_callback(self.enable_tune_ppm_checkbox)

    def get_dec_tune(self):
        return self.dec_tune

    def set_dec_tune(self, dec_tune):
        self.dec_tune = dec_tune
        self.analog_quadrature_demod_cf_0.set_gain(self.samp_rate/self.dec_xlate/self.dec_tune/(2*math.pi*4800))



def main(top_block_cls=rstt_rx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
