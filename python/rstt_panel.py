#!/usr/bin/env python

import numpy as np

import matplotlib
matplotlib.use("QT5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.figure import Figure

from gnuradio import gr, blocks

from PyQt5 import Qt, QtCore, QtWidgets

from calibration import CalibrationCollector, Calibration
from frame import Frame
from struct import unpack
from subframe import SF_TYPE_CONFIG, SF_TYPE_MEASUREMENTS, SF_TYPE_GPS, SF_TYPE_PADDING, SF_TYPE_WTF1

class RsttCanvas(FigureCanvas):
	"""Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

	def __init__(self, parent=None, width=5, height=4, dpi=100):
		fig = Figure(figsize=(width, height), dpi=dpi)
		self.a = fig.add_subplot(111)
		# We want the axes cleared every time plot() is called
		self.a.set_title("Temperature")
		self.x = []
		self.temp = []
		self.hum = []
		self.pres = []

		FigureCanvas.__init__(self, fig)
		self.setParent(parent)

		FigureCanvas.setSizePolicy(self,
				QtWidgets.QSizePolicy.Expanding,
				QtWidgets.QSizePolicy.Expanding)
		FigureCanvas.updateGeometry(self)

	def update_figure(self, num, temp, hum, pres):
		self.x.append(num)
		self.temp.append(temp)
		self.hum.append(hum)
		self.pres.append(pres)

		self.a.hold(False)
		self.a.plot(self.x, self.temp)
		self.a.hold(True)
		self.a.plot(self.x, self.hum)
		self.a.plot(self.x, self.pres)
		self.a.legend(('temp', 'humidity', 'pressure'), loc=2)
		self.a.set_xlim(num-60, num)

		self.draw()


class rsttPanel(gr.sync_block, QtWidgets.QWidget):
	def __init__(self, *args, **kwds):
		gr.sync_block.__init__(
			self,
			name = "rstt_panel",
			in_sig = [(np.int16, 240)],
			out_sig = None,
		)

		QtWidgets.QWidget.__init__(self)

		vlayout = Qt.QVBoxLayout()
		layout = Qt.QHBoxLayout()

		label_nr = Qt.QLabel("Frame Nr")
		self.frame_num = Qt.QLabel("xxx")
                self.frame_num.setStyleSheet("font-weight: bold")

		label_node = Qt.QLabel("Node ID")
		self.node_id = Qt.QLabel("xxxxxxxx")
                self.node_id.setStyleSheet("font-weight: bold")

		self.calibrated_label = Qt.QLabel("not calibrated")
                self.calibrated_label.setStyleSheet("font-weight:bold; color: red")

		plotWidget = QtWidgets.QWidget(self)
		self.plot = RsttCanvas(plotWidget, width=5, height=4, dpi=100)

		layout.addWidget(label_nr)
		layout.addWidget(self.frame_num)
		layout.addWidget(label_node)
		layout.addWidget(self.node_id)
		layout.addWidget(self.calibrated_label)

		vlayout.addWidget(self.plot)
		vlayout.addLayout(layout)
		self.setLayout(vlayout)

		self.calib = CalibrationCollector()
		self.frame_prev = None
		self.calibrated = False
		self.conf = None

	def work(self, input_items, output_items):
		inp = input_items[0]

		for i in range(len(inp)):
			data = []
			for x in inp[i]:
				data.append(x&0xFF)
				data.append(x>>8)

			frame = Frame(data, self.frame_prev)
			if not frame:
				print "no frame" + str(frame)
				continue
			if not frame.is_broken():
				self.frame_prev = frame

			self.conf = frame.get(SF_TYPE_CONFIG)
			if self.conf is not None:
				frame_num = self.conf.frame_num
				node_id   = self.conf.id
				calibration_num = self.conf.calibration_num

				self.node_id.setText(str(node_id))
				self.frame_num.setText(str(frame_num))
			else:
				frame_num = 0

			self.meas = frame.get(SF_TYPE_MEASUREMENTS)
			if self.meas is not None and self.conf is not None:
				temp = self.meas.temp
				hum  = self.meas.hum_down
				pres = self.meas.pressure

				self.plot.update_figure(frame_num, temp, hum, pres)

			if not self.calibrated and self.conf is not None:
				self.calibrated = self.calib.addFragment(self.conf.calibration_num, self.conf.calibration_data)
				if self.calibrated:
					print("calibration complete at frame %s" % frame_num)
					calib_data = self.calib.data()
					self.calib = Calibration(calib_data)

					self.calibrated_label.setText("calibrated")
					self.calibrated_label.setStyleSheet("color: green")

			print("frame: %s %s" % (frame_num, not frame.is_broken(), ))


		return len(inp)

