#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx, widgets
from scene import Scene
from levelswizard import LevelsWizard
from liftswizard import LiftsWizard

class SceneWizard(wx.Dialog):
	def __init__(self, parent, scene, id = -1, title = "Scene Wizard"):
		wx.Dialog.__init__(self, parent, id, title, size = (500,300))

		# Escena que controla los datos
		self.__scene = scene

		# Definición de páginas
		self.__levelsWizard = LevelsWizard(self, self.__scene, self.CheckSelectLevelsHandler)

		# Añadimos las páginas
		self.__sizerU = wx.BoxSizer(wx.HORIZONTAL)
		self.__sizerU.Add(self.__levelsWizard, 1, wx.EXPAND)

		self.__state = 0
		self.__sizerU.Show(self.__levelsWizard, True, True)

		# Boton de siguiente y cancelar
		self.__nextButton = wx.Button(self, widgets.ID_WIZARD_NEXTBUTTON, "Next >>")
		self.__nextButton.Disable()
		wx.EVT_BUTTON(self, widgets.ID_WIZARD_NEXTBUTTON, self.__OnNextButton)
		self.__cancelButton = wx.Button(self, widgets.ID_WIZARD_CANCELBUTTON, "Cancel")
		wx.EVT_BUTTON(self, widgets.ID_WIZARD_CANCELBUTTON, self.__OnCancelButton)

		self.__sizerD = wx.BoxSizer(wx.HORIZONTAL)
		self.__sizerD.Add(self.__cancelButton, 1, wx.EXPAND)
		self.__sizerD.Add(self.__nextButton, 1, wx.EXPAND)

		self.__sizer = wx.BoxSizer(wx.VERTICAL)
		self.__sizer.Add(self.__sizerU, 1, wx.EXPAND)
		self.__sizer.Add(self.__sizerD, 0, wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.__sizer)
		self.Layout()

	def GetScene(self):
		return self.__scene

	def CheckSelectLevelsHandler(self):
		if self.__scene.AreAllLevelsSelected():
			self.__nextButton.Enable()
			return True
		return False

	def CheckSelectLiftsHandler(self):
		if self.__scene.AreAllLiftsSelected():
			self.__nextButton.Enable()
			return True
		return False

	def __OnNextButton(self, event):
		if self.__state == 0:
			#if self.__levelsWizard.GetNumberOfLevelsSelected() == self.__scene.GetMaxLevels():
				#try:
					#self.__scene.SelectLevels(self.__levelsWizard.GetSelectedLevels())
				#except Exception, e:
					#print e
					#return
			self.__liftsWizard = LiftsWizard(self, self.__scene, self.CheckSelectLiftsHandler)
			self.__sizerU.Add(self.__liftsWizard, 1, wx.EXPAND)
			self.__sizerU.Show(self.__levelsWizard, False, True)
			self.__sizerU.Show(self.__liftsWizard, True, True)
			if not self.CheckSelectLiftsHandler():
				self.__nextButton.Disable()
			self.Layout()
			self.__state = 1
		elif self.__state == 1:
			self.__scene.Finalize()
			import os.path
			path = os.path.abspath(os.path.curdir)
			d = wx.FileDialog(self, "Save scene", defaultDir = path + "/scenes", wildcard = "*.scn4", style = wx.SAVE | wx.OVERWRITE_PROMPT)
			if d.ShowModal() == wx.ID_OK:
				filename = path + '/scenes/' + d.GetFilename()
				if filename.find('scn4') == -1:
					filename += '.scn4'
				try:
					file = open(filename, "w+")
					print filename
					self.__scene.ToXML(file)
					file.close()
				except Exception, e:
					print "Excepcion: ", e
					error = wx.MessageDialog(self, "Error saving scene.", "Exception", style = wx.ICON_ERROR | wx.OK)
					error.ShowModal()
					error.Destroy()
			d.Destroy()
			self.EndModal(0)

	def __OnCancelButton(self, event):
		self.EndModal(-1)
