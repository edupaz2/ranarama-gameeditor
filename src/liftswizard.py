
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx

class LiftsWizard(wx.Panel):
	def __init__(self, parent, scene, checkEndHandler):
		wx.Panel.__init__(self, parent)

		self.__checkEndHandler = checkEndHandler

		self.__scene = scene

		self.__listOfAllLifts = self.__scene.GetSelectedLifts()# lista de ascensores por cada nivel
		self.__listOfLiftsNotConnected = [] # lista de ascensores sin asignar relacion
		for elem in self.__listOfAllLifts:
			self.__listOfLiftsNotConnected.append(list(elem))

		self.__levelFrom = -1
		self.__liftFrom = -1
		self.__levelTo = -1
		self.__liftTo = -1

		self.__liftsFrom = []
		self.__liftsTo = []

		self.__listctrl = wx.ListCtrl(self, 100, style =  wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_VRULES| wx.LC_HRULES)
		self.__listctrl.InsertColumn(0, "Level From")
		self.__listctrl.InsertColumn(1, "Lift From")
		self.__listctrl.InsertColumn(2, "Level To")
		self.__listctrl.InsertColumn(3, "Lift To")

		self.__levelFromCB = wx.ComboBox(self, 101, "", choices = self.__ParseLevelList(self.__listOfLiftsNotConnected), style = wx.CB_DROPDOWN | wx.CB_READONLY)
		wx.EVT_COMBOBOX(self, 101, self.OnLevelFrom)
		self.__liftFromCB = wx.ComboBox(self, 102, "", choices = [], style = wx.CB_DROPDOWN | wx.CB_READONLY)
		wx.EVT_COMBOBOX(self, 102, self.OnLiftFrom)
		self.__levelToCB = wx.ComboBox(self, 103, "", choices = [], style = wx.CB_DROPDOWN | wx.CB_READONLY)
		wx.EVT_COMBOBOX(self, 103, self.OnLevelTo)
		self.__liftToCB = wx.ComboBox(self, 104, "", choices = [], style = wx.CB_DROPDOWN | wx.CB_READONLY)
		wx.EVT_COMBOBOX(self, 104, self.OnLiftTo)

		self.__ok = wx.Button(self, 105, "Add Relationship")
		wx.EVT_BUTTON(self, 105, self.OnOk)

		self.__levelFromH = wx.StaticText(self, -1, "Origin Level")
		self.__liftFromH = wx.StaticText(self, -1, "Origin Lift")
		self.__levelToH = wx.StaticText(self, -1, "Destiny Level")
		self.__liftToH = wx.StaticText(self, -1, "Destiny Lift")

		sizerH = wx.BoxSizer(wx.HORIZONTAL)
		sizerH.Add(self.__levelFromH, 1, wx.EXPAND)
		sizerH.Add(self.__liftFromH, 1, wx.EXPAND)
		sizerH.Add(self.__levelToH, 1, wx.EXPAND)
		sizerH.Add(self.__liftToH, 1, wx.EXPAND)

		sizerD = wx.BoxSizer(wx.HORIZONTAL)
		sizerD.Add(self.__levelFromCB, 1, wx.EXPAND)
		sizerD.Add(self.__liftFromCB, 1, wx.EXPAND)
		sizerD.Add(self.__levelToCB, 1, wx.EXPAND)
		sizerD.Add(self.__liftToCB, 1, wx.EXPAND)

		#help = wx.StaticText(self, -1, "Wizard de seleccion de ascensores.\n Por favor, seleccione, en este orden, nivel de origen->ascensor de origen->nivel de destino->ascensor de destino.")
		help = wx.StaticText(self, -1, "Lift selection wizard.\n Please select, in this order, origin level, origin lift, destiny level, destiny lift and then press Add.\n Press Next when you finish.")

		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(help, 0, wx.EXPAND)
		sizer.Add(self.__listctrl, 1, wx.EXPAND)
		sizer.Add(sizerH, 0, wx.EXPAND)
		sizer.Add(sizerD, 0, wx.EXPAND)
		sizer.Add(self.__ok, 0, wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(sizer)
		self.Layout()

	def __ParseLevelList(self, levellist):
		tmp = []
		for level in range(len(levellist)):
			tmp.append(str(level + 1))
		return tmp

	def __ParseLiftList(self, liftlist):
		tmp = []
		for lift in liftlist:
			tmp.append(str(lift.getLiftID()) + ' (' + str(lift.getRowPos()) + ',' + str(lift.getColPos()) + ')')
		return tmp

	def __ResetLevelFrom(self):
		self.__levelFrom = -1
		self.__levelFromCB.Clear()
		self.__levelFromCB.SetValue('')

	def __ResetLiftFrom(self):
		self.__liftFrom = -1
		del self.__liftsFrom[:]
		self.__liftFromCB.Clear()
		self.__liftFromCB.SetValue('')

	def __ResetLevelTo(self):
		self.__levelTo = -1
		self.__levelToCB.Clear()
		self.__levelToCB.SetValue('')

	def __ResetLiftTo(self):
		self.__liftTo = -1
		del self.__liftsTo[:]
		self.__liftToCB.Clear()
		self.__liftToCB.SetValue('')

	def OnLevelFrom(self, event):
		try:
			self.__levelFrom = int(self.__levelFromCB.GetValue()[0])
		except:
			self.__levelFrom = -1
			return

		# Reseteo el ascensor de origen y el nivel y ascensor de destino
		self.__ResetLiftFrom()
		self.__ResetLevelTo()
		self.__ResetLiftTo()

		# Meto los ascensores libres del nivel
		self.__liftsFrom = self.__ParseLiftList(self.__listOfLiftsNotConnected[self.__levelFrom - 1])
		for lift in self.__liftsFrom:
			self.__liftFromCB.Append(str(lift))
		self.__liftFromCB.SetValue('')

		# Meto el nivel de destino
		for level in self.__ParseLevelList(self.__listOfLiftsNotConnected):
			if int(level) != self.__levelFrom:
				self.__levelToCB.Append(str(level))
		self.__levelToCB.SetValue('')

	def OnLiftFrom(self, event):
		try:
			self.__liftFrom = int(self.__liftFromCB.GetValue()[0])
		except:
			self.__liftFrom = -1
			return

	def OnLevelTo(self, event):
		try:
			self.__levelTo = int(self.__levelToCB.GetValue()[0])
		except:
			self.__levelTo = -1
			return

		self.__ResetLiftTo()

		# Meto los niveles libres del nivel
		self.__liftsTo = self.__ParseLiftList(self.__listOfAllLifts[self.__levelTo - 1])# Aqui le paso todos los ascensores posibles del nivel
		for lift in self.__liftsTo:
			self.__liftToCB.Append(str(lift))
		self.__liftToCB.SetValue('')

	def OnLiftTo(self, event):
		try:
			self.__liftTo = int(self.__liftToCB.GetValue()[0])
		except:
			self.__liftTo = -1
			return

	def OnOk(self, event):
		#print self.__levelFrom,  self.__liftFrom, self.__levelTo, self.__liftTo
		if self.__levelFrom != -1 and self.__liftFrom != -1 and self.__levelTo != -1 and self.__liftTo != -1:
			try:
				self.__scene.SetConnection((self.__levelFrom, self.__liftFrom, self.__levelTo, self.__liftTo))
			except Exception, e:
				print e
				return
			else:
				#print "Tengo que eliminar de la lista de disponibles: nivel:", self.__levelFrom, ", ascensor: ", self.__liftTo
				index = 0
				for lift in self.__listOfLiftsNotConnected[self.__levelFrom - 1]:
					if lift.getLiftID() == self.__liftFrom:
						break
					index += 1
				self.__listOfLiftsNotConnected[self.__levelFrom - 1].pop(index)
	
				self.__listctrl.DeleteAllItems()
				connections = self.__scene.GetConnections()
				for i in range(len(connections)):
					connection = connections[i]
					self.__listctrl.InsertStringItem(i, str(connection[0]))
					self.__listctrl.SetStringItem(i, 1, str(connection[1]))
					self.__listctrl.SetStringItem(i, 2, str(connection[2]))
					self.__listctrl.SetStringItem(i, 3, str(connection[3]))
	
				self.__levelFromCB.SetValue('')
				self.__ResetLiftFrom()
				self.__ResetLevelTo()
				self.__ResetLiftTo()
	
				if self.__checkEndHandler():
					self.__ok.Disable()
					self.__levelFromCB.Disable()
					self.__liftFromCB.Disable()
					self.__levelToCB.Disable()
					self.__liftToCB.Disable()
	
				self.Refresh(False)
