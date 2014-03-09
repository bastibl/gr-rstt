#!/usr/bin/env python

import wx
import numpy as np
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
import matplotlib.cm as cm
from matplotlib.backends.backend_wxagg import NavigationToolbar2Wx, Toolbar, FigureCanvasWxAgg

from gnuradio import gr, blocks

from calibration import CalibrationCollector, Calibration
from frame import Frame
from struct import unpack
from subframe import SF_TYPE_CONFIG, SF_TYPE_MEASUREMENTS, SF_TYPE_GPS, SF_TYPE_PADDING, SF_TYPE_WTF1

EVENT_CALIBRATED = 0
EVENT_CONFIG     = 1
EVENT_MEASSURE   = 2

wxDATA_EVENT = wx.NewEventType()
def EVT_DATA_EVENT(win, func):
	win.Connect(-1, -1, wxDATA_EVENT, func)

class DataEvent(wx.PyEvent):
	def __init__(self, data):
		wx.PyEvent.__init__(self)
		self.SetEventType (wxDATA_EVENT)
		self.data = data

	def Clone (self):
		self.__class__ (self.GetId())

class rsttPanel(gr.sync_block):
	def __init__(self, *args, **kwds):
		gr.sync_block.__init__(
			self,
			name = "rstt_panel",
			in_sig = [(np.int16, 240)],
			out_sig = None,
		)

		self.panel = rsttWxPanel(*args, **kwds);
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
				de = DataEvent([EVENT_CONFIG, frame_num, node_id, calibration_num])
				wx.PostEvent(self.panel, de)
				del de
			else:
				frame_num = 'N/A'

			self.meas = frame.get(SF_TYPE_MEASUREMENTS)
			if self.meas is not None and self.conf is not None:
				temp = self.meas.temp
				hum  = self.meas.hum_down
				pres = self.meas.pressure
				de = DataEvent([EVENT_MEASSURE, self.conf.frame_num, temp, hum, pres])
				wx.PostEvent(self.panel, de)
				del de


			#self._dump_frame(frame, frame_num)
			#self._dump_eval(frame)
			if not self.calibrated and self.conf is not None:
				self.calibrated = self.calib.addFragment(self.conf.calibration_num, self.conf.calibration_data)
				if self.calibrated:
					print("calibration complete at frame %s" % frame_num)
					calib_data = self.calib.data()
					self.calib = Calibration(calib_data)

					de = DataEvent([EVENT_CALIBRATED])
					wx.PostEvent(self.panel, de)
					del de




			print("frame: %s %s" % (frame_num, not frame.is_broken(), ))


		return len(inp)

class rsttWxPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.label_1 = wx.StaticText(self, -1, "State")
		self.label_2 = wx.StaticText(self, -1, "Frame Nr")
		self.label_3 = wx.StaticText(self, -1, "Node ID")
		self.axes    = wx.CheckBox(self, -1, "auto Axes")
		self.axes.SetValue(1)

		self.calibrated = wx.StaticText(self, -1, "not calibrated")
		self.frame_num = wx.StaticText(self, -1, "xxxxxxxx")
		self.node_id = wx.StaticText(self, -1, "xxxxxxxxxxx")

		self.fig = Figure((5,4), 75)
		self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
		self.toolbar = NavigationToolbar2Wx(self.canvas)

		self.__set_properties()
		self.__do_layout()
		self.__init_plot()
		self.toolbar.Realize()
		EVT_DATA_EVENT (self, self.display_data)

	def __set_properties(self):
		font_bold = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")
		font_normal = wx.Font(16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, "")
		font_small = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, "")

		self.calibrated.SetFont(font_bold)
		self.calibrated.SetForegroundColour(wx.RED)
		self.frame_num.SetFont(font_bold)
		self.node_id.SetFont(font_bold)

	def __do_layout(self):
		sizer_0 = wx.BoxSizer(wx.VERTICAL)
		sizer_1 = wx.BoxSizer(wx.HORIZONTAL)

		flag = wx.ALIGN_CENTER_VERTICAL|wx.LEFT

		# arguments: window, proportion, flag, border
		sizer_1.Add(self.label_1, 0, flag)
		sizer_1.Add(self.calibrated, 0, flag, 20)
		sizer_1.Add(self.label_2, 0, flag, 20)
		sizer_1.Add(self.frame_num, 0, flag, 20)
		sizer_1.Add(self.label_3, 0, flag, 20)
		sizer_1.Add(self.node_id, 0, flag, 20)
		sizer_0.Add(sizer_1, 1, wx.ALIGN_CENTER)
		sizer_0.Add(self.canvas, 0, wx.ALIGN_CENTER | wx.GROW)
		sizer_0.Add(self.toolbar, 0, wx.ALIGN_CENTER)
		sizer_0.Add(self.axes, 0, wx.ALIGN_CENTER)

		self.SetSizer(sizer_0)

	def __init_plot(self):
		self.a = self.fig.add_subplot(111)
		self.a.set_title("Temperature")
		self.x = []
		self.temp = []
		self.hum = []
		self.pres = []
		self.plots = [self.a.plot([],[], linewidth=2)[0] for x in range(3)]
		self.a.legend(('temp', 'humidity', 'pressure'), loc=2)

	def GetToolBar(self):
		return self.toolbar

	def display_data(self, event):
		msg_type = event.data[0]
		msg = event.data

		if msg_type == EVENT_CALIBRATED:
			self.calibrated.SetLabel("calibrated")
			self.calibrated.SetForegroundColour('#005000')
		elif msg_type == EVENT_CONFIG:
			self.frame_num.SetLabel(str(msg[1]))
			self.node_id.SetLabel(msg[2])
		elif msg_type == EVENT_MEASSURE:
			self.x.append(msg[1])
			self.temp.append(msg[2])
			self.hum.append(msg[3])
			self.pres.append(msg[4])

			for i in range(3):
				self.plots[i].set_xdata(self.x)
			self.plots[0].set_ydata(self.temp)
			self.plots[1].set_ydata(self.hum)
			self.plots[2].set_ydata(self.pres)

			if self.axes.IsChecked():
				allData = self.hum + self.pres + self.temp
				self.a.set_xlim([min(self.x) - 1, max(self.x)])
				self.a.set_ylim([min(allData)*.95, max(allData)*1.05])
			self.canvas.draw()


		self.Layout()

	def clear_data(self):
		self.program_information.SetLabel("xxxx")
		self.frame_num.SetLabel("xxxxxxxx")
		self.node_id.SetLabel("xxxxxxxxxxx")

