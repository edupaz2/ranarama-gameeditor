#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx

class Presentation(wx.Dialog):
	def __init__(self, parent, id = -1, title = "Editor - Rök Studios"):
		wx.Dialog.__init__(self, parent, id, title, size=(wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X), wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)))

		self.ShowFullScreen(True)

		image = wx.Image("images/RokStudios.jpg")
		self.rokImage = wx.BitmapFromImage(image.Scale(600,720))
		self.InitBuffer()

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.Bind(wx.EVT_LEFT_DOWN, self.Exit)
		self.Bind(wx.EVT_RIGHT_DOWN, self.Exit)
		self.Bind(wx.EVT_MIDDLE_DOWN, self.Exit)

		self.SetAutoLayout(True)
		#self.SetSizer(self.__sizer)
		self.Layout()

	def InitBuffer(self):
		size = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(size.width, size.height)
		dc = wx.BufferedDC(None, self.buffer)
		self.Draw(dc)
		self.reInitBuffer = False

	def Draw(self, dc):
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		dc.BeginDrawing()
		dc.DrawBitmap(self.rokImage, (wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X) - self.rokImage.GetWidth()) / 2, (wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y) - self.rokImage.GetHeight()) / 2)
		dc.EndDrawing()

	def OnSize(self, event):
		self.reInitBuffer = True

	def OnIdle(self, event):
		if self.reInitBuffer:
			self.InitBuffer()
			self.Refresh(False)

	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer)
		self.Draw(dc)

	def Exit(self, event):
		self.EndModal(0)
