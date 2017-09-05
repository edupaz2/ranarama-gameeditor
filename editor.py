#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Obtengo la ruta de ejecución y añado al path los modulos propios
import os, sys
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(path + '/src')

import wx
import widgets
from levelsmanagerpage import LevelsManagerPage
from levelpage import LevelPage

statusbar = None

class Editor(wx.Frame):
	def __init__(self, parent = None):
		wx.Frame.__init__(self, parent, title = "Map Editor", style = wx.DEFAULT_FRAME_STYLE)

		self.ShowFullScreen(True)

		self.__statusbar = self.CreateStatusBar() # A StatusBar in the bottom of the window
		# File menu.
		filemenu = wx.Menu()
		#filemenu.Append(widgets.ID_EDITOR_NEWMAP, "&New map","Crea un nuevo mapa")
		#filemenu.AppendSeparator()
		filemenu.Append(widgets.ID_EDITOR_EXIT,"E&xit","Terminate the program")
		# Help menu.
		helpmenu = wx.Menu()
		helpmenu.Append(widgets.ID_EDITOR_ABOUT, "&About","Information about this program")
		# Creating the menubar.
		menuBar = wx.MenuBar()
		menuBar.Append(filemenu,"&File")
		menuBar.Append(helpmenu,"&Help")
		
		self.SetMenuBar(menuBar)
		wx.EVT_MENU(self, widgets.ID_EDITOR_EXIT, self.OnExit)
		wx.EVT_MENU(self, widgets.ID_EDITOR_ABOUT, self.OnAbout)

		self.notebook = wx.Notebook(self, widgets.ID_EDITOR_NOTEBOOK, style = wx.NB_TOP)
		wx.EVT_NOTEBOOK_PAGE_CHANGED(self, widgets.ID_EDITOR_NOTEBOOK, self.OnPageChanged)

		self.__levelManagerPage = LevelsManagerPage(self.notebook, self.CreateNewLevelPage, self.ChangePageName, self.__statusbar)
		self.notebook.AddPage(self.__levelManagerPage, "Levels Manager")

	def CreateNewLevelPage(self, level):
		levelpage = LevelPage(self.notebook, level, self.__statusbar)
		self.notebook.AddPage(levelpage, level.getName())
		self.notebook.GetCurrentPage().Refresh(False)

	def ChangePageName(self, pageid, name):
		self.notebook.SetPageText(pageid + 1, name)

	def OnAbout(self, event):
		d = wx.MessageDialog(self, "Map editor for Game Ramarana made by group 4\nJaime Cornejo, David Fuentes y Eduardo Paz\n\n\nMáster de Desarrollo de Videojuegos UCM 2006/2007","About Map Editor", wx.OK) # Create a message dialog box
		d.ShowModal() # Shows it
		d.Destroy() # finally destroy it when finished.

	def OnExit(self,event):
		self.Close(True)  # Close the frame.

	def OnPageChanged(self, event):
		if event.GetSelection() == 0:
			self.__statusbar.PushStatusText("")
			self.__levelManagerPage.FillList()

if __name__=="__main__":
	app = wx.App()
	from presentation import Presentation
	presentation = Presentation(None)
	presentation.ShowModal()
	presentation.Destroy()
	editor = Editor()
	editor.Show()
	app.MainLoop()
