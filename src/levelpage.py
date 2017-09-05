#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
import widgets, entityfactory, entity
from graphiclevel import GraphicLevel
from levelview import LevelView

class LevelPage(wx.Panel):
	def __init__(self, parent, level, statusbar):
		wx.Panel.__init__(self, parent)#, style = wx.RAISED_BORDER)#wx.FULL_REPAINT_ON_RESIZE)

		self.__graphiclevel = GraphicLevel(level)
		self.__statusbar = statusbar

		#### Modos
		self.__normalBitmap = wx.Bitmap("images/normal.png")
		self.__normalButton = wx.BitmapButton(self, widgets.ID_LEVEL_NORMALBUTTON, self.__normalBitmap, size = wx.Size(30,30))
		self.__normalButtonToolTip = wx.ToolTip("Normal Mode")
		self.__normalButton.SetToolTip(self.__normalButtonToolTip)
		#self.__normalButton.Disable()
		wx.EVT_BUTTON(self, widgets.ID_LEVEL_NORMALBUTTON, self.OnNormalButton)

		self.__paintBitmap = wx.Bitmap("images/paint.png")
		self.__paintButton = wx.BitmapButton(self, widgets.ID_LEVEL_PAINTBUTTON, self.__paintBitmap, size = wx.Size(30,30))
		self.__paintButtonToolTip = wx.ToolTip("Paint Mode")
		self.__paintButton.SetToolTip(self.__paintButtonToolTip)
		wx.EVT_BUTTON(self, widgets.ID_LEVEL_PAINTBUTTON, self.OnPaintButton)

		self.__modeButtonBox = wx.StaticBox(self, -1, self.__normalButtonToolTip.GetTip())
		self.__modeButtonSizer = wx.StaticBoxSizer(self.__modeButtonBox, wx.HORIZONTAL)
		self.__modeButtonSizer.Add(self.__normalButton, 1, flag = wx.EXPAND)
		self.__modeButtonSizer.Add(self.__paintButton, 1, flag = wx.EXPAND)

		##### Acciones del modo normal
		#self.__selectBitmap = wx.Bitmap("images/select.png")
		#self.__selectButton = wx.BitmapButton(self, widgets.ID_LEVEL_SELECTBUTTON, self.__selectBitmap, size = wx.Size(30,30))
		#self.__selectButtonToolTip = wx.ToolTip("Select")
		#self.__selectButton.SetToolTip(self.__selectButtonToolTip)
		#wx.EVT_BUTTON(self, widgets.ID_LEVEL_SELECTBUTTON, self.OnSelectButton)

		self.__eraseBitmap = wx.Bitmap("images/erase.png")
		self.__eraseButton = wx.BitmapButton(self, widgets.ID_LEVEL_ERASEBUTTON, self.__eraseBitmap, size = wx.Size(30,30))
		self.__eraseButtonToolTip = wx.ToolTip("Erase")
		self.__eraseButton.SetToolTip(self.__eraseButtonToolTip)
		wx.EVT_BUTTON(self, widgets.ID_LEVEL_ERASEBUTTON, self.OnEraseButton)
		#self.__eraseButton.Disable()

		#self.__copyBitmap = wx.Bitmap("images/copy.png")
		#self.__copyButton = wx.BitmapButton(self, widgets.ID_LEVEL_COPYBUTTON, self.__copyBitmap, size = wx.Size(30,30))
		#self.__copyButtonToolTip = wx.ToolTip("Copy")
		#self.__copyButton.SetToolTip(self.__copyButtonToolTip)
		#wx.EVT_BUTTON(self, widgets.ID_LEVEL_COPYBUTTON, self.OnCopyButton)
		#self.__copyButton.Disable()

		#self.__pasteBitmap = wx.Bitmap("images/paste.png")
		#self.__pasteButton = wx.BitmapButton(self, widgets.ID_LEVEL_PASTEBUTTON, self.__pasteBitmap, size = wx.Size(30,30))
		#self.__pasteButtonToolTip = wx.ToolTip("Paste")
		#self.__pasteButton.SetToolTip(self.__pasteButtonToolTip)
		#wx.EVT_BUTTON(self, widgets.ID_LEVEL_PASTEBUTTON, self.OnPasteButton)
		#self.__pasteButton.Disable()

		self.__normalGridSizer = wx.GridSizer(0,3)
		#self.__normalGridSizer.Add(self.__selectButton, 1, wx.EXPAND)
		self.__normalGridSizer.Add(self.__eraseButton, 1, wx.EXPAND)
		#self.__normalGridSizer.Add(self.__copyButton, 1, wx.EXPAND)
		#self.__normalGridSizer.Add(self.__pasteButton, 1, wx.EXPAND)

		self.__normalActionButtonsSizer = wx.BoxSizer(wx.VERTICAL)
		self.__normalActionButtonsSizer.Add(self.__normalGridSizer, 1, wx.EXPAND)

		#### Acciones del modo paint
		self.valueTileList = entity.entitytypes		
		self.__typeOfEntity = wx.ComboBox(self, widgets.ID_LEVEL_COMBOBOX, "", wx.Point(150, 90), wx.Size(95, -1), self.valueTileList, wx.CB_DROPDOWN)
		wx.EVT_COMBOBOX(self, widgets.ID_LEVEL_COMBOBOX, self.OnComboBox)

		self.__gridBitmap = wx.Bitmap("images/grid.png")
		self.__gridButton = wx.BitmapButton(self, widgets.ID_LEVEL_GRIDBUTTON, self.__gridBitmap, size = wx.Size(30,30))
		self.__gridButtonToolTip = wx.ToolTip("Show grid")
		self.__gridButton.SetToolTip(self.__gridButtonToolTip)
		wx.EVT_BUTTON(self, widgets.ID_LEVEL_GRIDBUTTON, self.OnGridButton)

		self.__paintGridSizer = wx.BoxSizer(wx.VERTICAL)
		self.__paintGridSizer.Add(self.__gridButton, 0, wx.EXPAND)

		self.__paintActionButtonsSizer = wx.BoxSizer(wx.VERTICAL)
		self.__paintActionButtonsSizer.Add(self.__typeOfEntity, 1, wx.EXPAND)
		self.__paintActionButtonsSizer.Add(self.__paintGridSizer, 1, wx.EXPAND)

		#### Sizer que contiene las acciones
		self.__actionsButtonBox = wx.StaticBox(self, -1, "Actions")
		self.__actionsButtonSizer = wx.StaticBoxSizer(self.__actionsButtonBox, wx.VERTICAL)
		self.__actionsButtonSizer.Add(self.__normalActionButtonsSizer)
		self.__actionsButtonSizer.Add(self.__paintActionButtonsSizer)
		# Oculto las opciones del modo paint
		self.__actionsButtonSizer.Show(self.__normalActionButtonsSizer, True, True)
		self.__actionsButtonSizer.Show(self.__paintActionButtonsSizer, False, True)

		#### Acciones de vista del mapa
		self.__centerButton = wx.Button(self, widgets.ID_LEVEL_CENTERBUTTON, "Center Map")
		wx.EVT_BUTTON(self, widgets.ID_LEVEL_CENTERBUTTON, self.OnCenterMap)

		zoomForLevel = 1
		self.__zoomSlider = wx.Slider(self, widgets.ID_LEVEL_ZOOMSLIDER, zoomForLevel, 1, 100)
		wx.EVT_SCROLL_CHANGED(self.__zoomSlider, self.OnSliderChanged)

		self.__viewBox = wx.StaticBox(self, widgets.ID_LEVEL_VIEWINGBOX, "Viewing")
		self.__viewSizer = wx.StaticBoxSizer(self.__viewBox, wx.VERTICAL)
		self.__viewSizer.Add(self.__centerButton, 1, wx.EXPAND)
		self.__viewSizer.Add(self.__zoomSlider, 1, wx.EXPAND)

		# Propiedades
		#self.__orientationLabel = wx.StaticText(self, -1, "Orientation: ")
		#self.__propertiesBox = wx.StaticBox(self, widgets.ID_LEVEL_PROPERTIESBOX, "Properties")
		#self.__propertiesSizer = wx.StaticBoxSizer(self.__propertiesBox, wx.VERTICAL)
		#self.__propertiesSizer.Add(self.__orientationLabel)

		# Panel de pintado del mapa
		self.__mapview = LevelView(self, self.__graphiclevel, self.__statusbar)#, self.__EntityPropertiesChangedHandler)
		self.__mapview.SetZoom(zoomForLevel)

		# Contenedores: left: para los modos, acciones y demás. right para el panel de pintado del mapa
		self.sizerLeft = wx.BoxSizer(wx.VERTICAL)
		self.sizerRight = wx.BoxSizer(wx.VERTICAL)

		self.sizerLeft.Add(self.__modeButtonSizer, 0, wx.EXPAND)
		self.sizerLeft.Add(self.__actionsButtonSizer, 0, wx.EXPAND)
		self.sizerLeft.Add(self.__viewSizer, 0, wx.EXPAND)
		#self.sizerLeft.Add(self.__propertiesSizer, 0, wx.EXPAND)

		self.sizerRight.Add(self.__mapview, proportion = 1, flag = wx.EXPAND | wx.ALL)

		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.sizerLeft)
		self.sizer.Add(self.sizerRight, 1, wx.EXPAND)

		self.SetAutoLayout(True)
		self.sizer.SetSizeHints(self)
		self.SetSizer(self.sizer)
		self.Layout()

	def OnNormalButton(self, event):
		self.__modeButtonBox.SetLabel(self.__normalButtonToolTip.GetTip())
		self.__actionsButtonSizer.Show(self.__normalActionButtonsSizer, True, True)
		self.__actionsButtonSizer.Show(self.__paintActionButtonsSizer, False, True)
		self.__actionsButtonSizer.Layout()
		self.sizerLeft.Layout()
		self.Refresh(False)
		self.__mapview.SetNormalMode()

	def OnPaintButton(self, event):
		self.__modeButtonBox.SetLabel(self.__paintButtonToolTip.GetTip())
		self.__actionsButtonSizer.Show(self.__normalActionButtonsSizer, False, True)
		self.__actionsButtonSizer.Show(self.__paintActionButtonsSizer, True, True)
		self.__actionsButtonSizer.Layout()
		self.__viewSizer.Layout()
		self.sizerLeft.Layout()
		self.__mapview.SetEditMode()

	def OnGridButton(self, event):
		if self.__graphiclevel.viewGrid():
			self.__graphiclevel.setViewGrid(False)
		else:
			self.__graphiclevel.setViewGrid(True)
		self.__mapview.Refresh(False)

	def OnEraseButton(self, event):
		self.__graphiclevel.eraseSelection()
		self.__mapview.Refresh(False)

	def OnCopyButton(self, event):
		pass

	def OnPasteButton(self, event):
		pass

	#def __EntityPropertiesChangedHandler(self, entityType):
		#print entityType
		#self.__orientationLabel.SetLabel("Orientation: " + entityType)

	def OnSliderChanged(self, event):
		value = self.__zoomSlider.GetValue()
		self.__mapview.SetZoom(value)
		self.__mapview.Refresh(False)

	def OnCenterMap(self, event):
		self.__mapview.CenterMap()
		self.__mapview.Refresh(False)

	def OnComboBox(self, event):
		value = event.GetString()
		self.__graphiclevel.setTypeOfEntityToPlace(value)
