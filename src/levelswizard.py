#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx

class LevelsWizard(wx.Panel):
	def __init__(self, parent, scene, checkEndHandler):
		wx.Panel.__init__(self, parent)

		self.__indexL = -1
		self.__indexR = -1
		self.__scene = scene
		self.__levels = scene.GetNameOfLevels()
		self.__levelsAdded = []

		self.__checkEndHandler = checkEndHandler

		self.__listctrl1 = wx.ListCtrl(self, 100, style =  wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_VRULES| wx.LC_HRULES)
		self.__listctrl1.InsertColumn(0, "Name")

		wx.EVT_LIST_ITEM_SELECTED(self, 100, self.OnItemSelected)

		for i in range(len(self.__levels)):
			level = self.__levels[i]
			self.__listctrl1.InsertStringItem(i, level)

		self.__add = wx.Button(self, 101, "Add")
		wx.EVT_BUTTON(self, 101, self.OnAdd)
		
		sizerL = wx.BoxSizer(wx.VERTICAL)
		sizerL.Add(self.__listctrl1, 1, wx.EXPAND)
		sizerL.Add(self.__add, 0, wx.EXPAND)

		self.__listctrl2 = wx.ListCtrl(self, 110, style = wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_VRULES| wx.LC_HRULES)
		self.__listctrl2.InsertColumn(0, "Level")
		self.__listctrl2.InsertColumn(1, "Name")

		wx.EVT_LIST_ITEM_SELECTED(self, 110, self.OnItemSelected)

		self.__up = wx.Button(self, 111, "Up")
		wx.EVT_BUTTON(self, 111, self.OnUp)
		self.__down = wx.Button(self, 112, "Down")
		wx.EVT_BUTTON(self, 112, self.OnDown)

		sizerRB = wx.BoxSizer(wx.VERTICAL)
		sizerRB.Add(self.__up, 0, wx.EXPAND)
		sizerRB.Add(self.__down, 0, wx.EXPAND)

		sizerR = wx.BoxSizer(wx.VERTICAL)
		sizerR.Add(self.__listctrl2, 1, wx.EXPAND)
		sizerR.Add(sizerRB, 0, wx.EXPAND)

		sizerD = wx.BoxSizer(wx.HORIZONTAL)
		sizerD.Add(sizerL, 1, wx.EXPAND)
		sizerD.Add(sizerR, 1, wx.EXPAND)

		#help = wx.StaticText(self, -1, "Wizard de seleccion de niveles.\n Por favor, seleccione los niveles que quiere exportar con el boton Add.")
		help = wx.StaticText(self, -1, "Level selection wizard.\n Please, select the levels you wish to export selecting them and pressing Add.\n Press Next when you finish.")
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(help, 0, wx.EXPAND)
		sizer.Add(sizerD, 1, wx.EXPAND)
		self.SetAutoLayout(True)
		self.SetSizer(sizer)
		self.Layout()

	def OnItemSelected(self, event):
		if event.GetId() == 100:
			self.__indexL = event.m_itemIndex
		elif event.GetId() == 110:
			self.__indexR = event.m_itemIndex

	def OnAdd(self, event):
		if self.__indexL != -1:
			try:
				self.__scene.SelectLevel(self.__levels[self.__indexL])
				#if len(self.__levelsAdded) < self.__scene.GetMaxLevels():# and self.__levelsAdded.count(self.__levels[self.__indexL]) == 0:
			except Exception, e:
				print e
				return
			else:
				self.__levelsAdded.append(self.__levels[self.__indexL])
				self.__indexR = len(self.__levelsAdded) - 1
				self.__FillList()
				
				if self.__checkEndHandler():
					self.__add.Disable()
					self.__up.Disable()
					self.__down.Disable()

	def OnUp(self, event):
		if self.__indexR > 0:
			self.__levelsAdded.insert(self.__indexR - 1, self.__levelsAdded.pop(self.__indexR))
			self.__indexR -= 1
			self.__FillList()

	def OnDown(self, event):
		if self.__indexR != -1 and self.__indexR < len(self.__levelsAdded) - 1:
			self.__levelsAdded.insert(self.__indexR + 1, self.__levelsAdded.pop(self.__indexR))
			self.__indexR += 1
			self.__FillList()

	def __FillList(self):
		self.__listctrl2.DeleteAllItems()
		for i in range(len(self.__levelsAdded)):
			level = self.__levelsAdded[i]
			self.__listctrl2.InsertStringItem(i, str(i + 1))
			self.__listctrl2.SetStringItem(i, 1, level)

	def GetNumberOfLevelsSelected(self):
		return len(self.__levelsAdded)

	def GetSelectedLevels(self):
		return self.__levelsAdded

