#!/usr/bin/env python
# -*- coding: utf-8 -*-

import wx
from levelpage import LevelPage
from levelsmanager import LevelsManager
import widgets

"""
Level Manager: controlará la importación,creación, salvado y duplicación de escenarios. Permitirá generar mapas.
"""
class LevelsManagerPage(wx.Panel):
	def __init__(self, parent, openLevelPageHandler, changePageNameHandler, statusbar = None):
		wx.Panel.__init__(self, parent)

		# Atributo principal
		self.__levelsManager = LevelsManager()

		# Atributos secundarios
		self.__itemSelected = -1
		self.__levelsEdited = []

		# Función para abrir un tab de level desde el padre
		self.__openLevelPage = openLevelPageHandler
		# Función para cambiar el nombre del tab
		self.__changePageNameHandler = changePageNameHandler
		# Statusbar para escribir lo que sea
		self.__statusbar = statusbar

		# Atributos visuales
		self.__levelList = wx.ListCtrl(self, widgets.ID_LEVELSMANAGER_LISTCTRL, style = wx.LC_REPORT|wx.SUNKEN_BORDER|wx.LC_SINGLE_SEL|wx.LC_VRULES| wx.LC_HRULES)
		wx.EVT_LIST_ITEM_SELECTED(self, widgets.ID_LEVELSMANAGER_LISTCTRL, self.OnItemSelected)

		self.__levelList.InsertColumn(0, "Level")
		self.__levelList.InsertColumn(1, "Modified")
		self.__levelList.InsertColumn(2, "Compiled")
		self.__levelList.InsertColumn(3, "Dimensions")
		self.__levelList.InsertColumn(4, "Author")

		self.__importButton = wx.Button(self, widgets.ID_LEVELSMANAGER_IMPORT, "Import")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_IMPORT, self.OnImport)

		self.__createButton = wx.Button(self, widgets.ID_LEVELSMANAGER_CREATE, "Create New")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_CREATE, self.OnCreate)

		self.__saveButton = wx.Button(self, widgets.ID_LEVELSMANAGER_SAVE, "Save")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_SAVE, self.OnSave)

		self.__editButton = wx.Button(self, widgets.ID_LEVELSMANAGER_EDIT, "Edit")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_EDIT, self.OnEdit)

		#self.__duplicateButton = wx.Button(self, widgets.ID_LEVELSMANAGER_DUPLICATE, "Duplicate")
		#wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_DUPLICATE, self.OnDuplicate)

		self.__changeNameButton = wx.Button(self, widgets.ID_LEVELSMANAGER_CHANGENAME, "Change Name")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_CHANGENAME, self.OnChangeName)

		self.__changeAuthorButton = wx.Button(self, widgets.ID_LEVELSMANAGER_CHANGEAUTHOR, "Change Author")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_CHANGEAUTHOR, self.OnChangeAuthor)

		self.__compileButton = wx.Button(self, widgets.ID_LEVELSMANAGER_COMPILE, "Compile")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_COMPILE, self.OnCompile)

		self.__generateSceneButton = wx.Button(self, widgets.ID_LEVELSMANAGER_GENERATESCENE, "Generate Scene")
		wx.EVT_BUTTON(self, widgets.ID_LEVELSMANAGER_GENERATESCENE, self.OnGenerateScene)

		self.__saveButton.Disable()
		self.__editButton.Disable()
		#self.__duplicateButton.Disable()
		self.__changeNameButton.Disable()
		self.__changeAuthorButton.Disable()
		self.__compileButton.Disable()

		self.__buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)

		self.__sizer = wx.BoxSizer(wx.VERTICAL)
		self.__sizer.Add(self.__levelList, 1, wx.EXPAND)
		self.__sizer.Add(self.__buttonsSizer, 0, wx.EXPAND)

		self.__buttonsSizer.Add(self.__importButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__createButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__saveButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__editButton, 1, wx.EXPAND)
		#self.__buttonsSizer.Add(self.__duplicateButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__changeNameButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__changeAuthorButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__compileButton, 1, wx.EXPAND)
		self.__buttonsSizer.Add(self.__generateSceneButton, 1, wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.__sizer)
		self.Layout()

	def OnImport(self, event):
		import os.path
		path = os.path.abspath(os.path.curdir)
		d = wx.FileDialog(self, "Import level", defaultDir = path + "/levels", wildcard = "*.lvl4", style = wx.OPEN)
		if d.ShowModal() == wx.ID_OK:
			try:
				filename = path + '/levels/' + d.GetFilename()
				if not self.__levelsManager.ImportLevelFromFile(filename):
					info = wx.MessageDialog(self, "Level already exists.", "Information", style = wx.ICON_INFORMATION | wx.OK)
					info.ShowModal()
					info.Destroy()
			except Exception, e:
				error = wx.MessageDialog(self, "Error while importing level.\n" + str(e), "Exception", style = wx.ICON_ERROR | wx.OK)
				error.ShowModal()
				error.Destroy()
			else:
				self.FillList()
		d.Destroy()

	def OnCreate(self, event):
		d = CreateNewLevelDialog(self, -1, "Create New Level")
		if d.ShowModal() == wx.ID_OK:
			try:
				rows = int(d.rows.GetValue())
				cols = int(d.cols.GetValue())
				#value = d.value #valor de inicializacion del escenario TODO!!!!!!
				name = d.name.GetValue()
				author = d.author.GetValue()

				if not self.__levelsManager.CreateNewLevel(name, rows, cols, author):
					info = wx.MessageDialog(self, "Level already exists.", "Information", style = wx.ICON_INFORMATION | wx.OK)
					info.ShowModal()
					info.Destroy()
				self.FillList()
			except Exception, e:
				error = wx.MessageDialog(self, "Error while creating level.\n" + str(e), "Exception", style = wx.ICON_ERROR | wx.OK)
				error.ShowModal()
				error.Destroy()
				return
		d.Destroy()

	def OnSave(self, event):
		if self.__itemSelected != -1:
			import os.path
			path = os.path.abspath(os.path.curdir)
			d = wx.FileDialog(self, "Save level", defaultDir = path + "/levels", wildcard = "*.lvl4", style = wx.SAVE)
			if d.ShowModal() == wx.ID_OK:
				filename = d.GetFilename()
				try:
					filename = path + '/levels/' + d.GetFilename()
					if filename.find('lvl4') == -1:
						filename += '.lvl4'
					file = open(filename, "w+")
					self.__levelsManager.SaveLevelToFile(self.__itemSelected, file)
					file.close()
				except Exception, e:
					error = wx.MessageDialog(self, "Error while saving level.\n" + str(e), "Exception", style = wx.ICON_ERROR | wx.OK)
					error.ShowModal()
					error.Destroy()
				else:
					self.FillList()
			d.Destroy()

	def OnEdit(self, event):
		if self.__itemSelected != -1:
			level = self.__levelsManager.GetLevel(self.__itemSelected)
			for levelEdited in self.__levelsEdited:
				if level.getName() == levelEdited:
					return
			self.__levelsEdited.append(level.getName())
			self.__openLevelPage(level)
			self.Refresh(False)

	#def OnDuplicate(self, event):
		#if self.__itemSelected != -1:
			#try:
				#self.__levelsManager.DuplicateLevel(self.__itemSelected)
			#except Exception, e:
				#print e
				#error = wx.MessageDialog(self, "Error while duplicating level.", "Exception", style = wx.ICON_ERROR | wx.OK)
				#error.ShowModal()
				#error.Destroy()
			#else:
				#self.FillList()

	def OnChangeName(self, event):
		if self.__itemSelected != -1:
			try:
				oldname = self.__levelsManager.GetLevelName(self.__itemSelected)
				d = wx.TextEntryDialog(self, "New map name", "Enter Name", oldname, style = wx.OK | wx.CANCEL)
				if d.ShowModal() == wx.ID_OK:
					newname = d.GetValue()
					self.__levelsManager.SetLevelName(self.__itemSelected, newname)
					try:
						oldindex = self.__levelsEdited.index(oldname)
						self.__changePageNameHandler(oldindex, newname)
					except ValueError:
						pass
				d.Destroy()
			except Exception, e:
				error = wx.MessageDialog(self, "Error while changing name.\n" + str(e), "Exception", style = wx.ICON_ERROR | wx.OK)
				error.ShowModal()
				error.Destroy()
			else:
				self.FillList()

	def OnChangeAuthor(self, event):
		if self.__itemSelected != -1:
			try:
				oldauthor = self.__levelsManager.GetLevelAuthor(self.__itemSelected)
				d = wx.TextEntryDialog(self, "New map author", "Enter Author", oldauthor, style = wx.OK | wx.CANCEL)
				if d.ShowModal() == wx.ID_OK:
					newauthor = d.GetValue()
					self.__levelsManager.SetLevelAuthor(self.__itemSelected, newauthor)
				d.Destroy()
			except Exception, e:
				error = wx.MessageDialog(self, "Error while changing author.\n" + str(e), "Exception", style = wx.ICON_ERROR | wx.OK)
				error.ShowModal()
				error.Destroy()
			else:
				self.FillList()

	def OnCompile(self, event):
		if self.__itemSelected != -1:
			try:
				level = self.__levelsManager.CompileLevel(self.__itemSelected)
			except Exception, e:
				error = wx.MessageDialog(self, "Error while compiling level.\n" + str(e), "Exception", style = wx.ICON_ERROR | wx.OK)
				error.ShowModal()
				error.Destroy()
			else:
				self.FillList()

	def OnGenerateScene(self, event):
		from scenewizard import SceneWizard
		from scene import Scene
		scene = Scene(self.__levelsManager.GetListOfLevels())
		wizard = SceneWizard(self, scene)
		wizard.ShowModal()
		#if wizard.ShowModal() == 0:
			##print "Scene saved"
			#return
		#print "CANCEL"

	def OnItemSelected(self, event):
		self.__itemSelected = event.m_itemIndex
		self.__saveButton.Enable()
		self.__editButton.Enable()
		#self.__duplicateButton.Enable()
		self.__changeNameButton.Enable()
		self.__changeAuthorButton.Enable()
		self.__compileButton.Enable()

	def FillList(self):
		self.__levelList.DeleteAllItems()
		levels = self.__levelsManager.GetListOfLevels()
		for i in range(len(levels)):
			level = levels[i]
			self.__levelList.InsertStringItem(i, level.getName())
			self.__levelList.SetStringItem(i, 1, str(level.getModified()))
			self.__levelList.SetStringItem(i, 2, str(level.getCompiled()))
			self.__levelList.SetStringItem(i, 3, str(level.getLength()) + "x" + str(level.getWidth()))
			self.__levelList.SetStringItem(i, 4, str(level.getAuthor()))
		self.Refresh(False)

class CreateNewLevelDialog(wx.Dialog):
	def __init__(self, parent, id, title):
		wx.Dialog.__init__(self, parent, id, title, size = (200,150))

		#self.dimensionsLabel = wx.StaticText(self, -1, "Dimensions")

		self.rowsLabel = wx.StaticText(self, -1, "Rows")
		self.rows = wx.TextCtrl(self, widgets.ID_MAP_ROWS)

		self.colsLabel = wx.StaticText(self, -1, "Columns")
		self.cols = wx.TextCtrl(self, widgets.ID_MAP_COLS)

		self.sizerRows = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerRows.Add(self.rowsLabel, 1, wx.EXPAND)
		self.sizerRows.Add(self.rows, 1, wx.EXPAND)

		self.sizerCols = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerCols.Add(self.colsLabel, 1, wx.EXPAND)
		self.sizerCols.Add(self.cols, 1, wx.EXPAND)

		self.nameLabel = wx.StaticText(self, -1, "Level Name")
		self.name = wx.TextCtrl(self, widgets.ID_MAP_NAME)

		self.sizerName = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerName.Add(self.nameLabel, 1, wx.EXPAND)
		self.sizerName.Add(self.name, 1, wx.EXPAND)

		self.authorLabel = wx.StaticText(self, -1, "Author")
		self.author = wx.TextCtrl(self, widgets.ID_MAP_AUTHOR, value = "Rok 8 Studios")

		self.authorName = wx.BoxSizer(wx.HORIZONTAL)
		self.authorName.Add(self.authorLabel, 1, wx.EXPAND)
		self.authorName.Add(self.author, 1, wx.EXPAND)

		self.buttons = self.CreateButtonSizer(wx.OK | wx.CANCEL)

		self.sizer = wx.BoxSizer(wx.VERTICAL)
		#self.sizer.Add(self.dimensionsLabel, 0, wx.EXPAND)
		self.sizer.Add(self.sizerRows, 1, wx.EXPAND)
		self.sizer.Add(self.sizerCols, 1, wx.EXPAND)
		self.sizer.Add(self.sizerName, 1, wx.EXPAND)
		self.sizer.Add(self.authorName, 1, wx.EXPAND)
		self.sizer.Add(self.buttons, 1, wx.EXPAND)

		self.SetAutoLayout(True)
		self.SetSizer(self.sizer)
		self.Layout()
