#!/usr/bin/env python
# -*- coding: utf-8 -*-
import wx
import widgets
from entity import entitytypes, orientations

class LevelView(wx.Panel):
	colours = ['Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple',
	'Brown', 'Aquamarine', 'Forest Green', 'Light Blue', 'Goldenrod',
	'Cyan', 'Orange', 'Navy', 'Dark Grey', 'Light Grey']

	def __init__(self, parent, graphiclevel, statusbar = None):
		wx.Panel.__init__(self, parent, style = wx.NO_FULL_REPAINT_ON_RESIZE)

		self.__graphiclevel = graphiclevel
		self.__mode = "NORMAL"
		self.__action = "none"
		self.__statusbar = statusbar

		self.__zoom = 1
		self.__paintSelectionBox = False
		self.__paintTileBoundingBox = False

		# Dos variables que nos ayudan a saber donde se pinta el mapa
		self.__initMapPoint = (0, 0)
		self.__centerMapPoint = (0, 0)
		self.__displacement = (0, 0)

		# Variables que ayudan en la captura de dos puntos del mapa, para su uso en diferentes acciones, como el pintado de cuadros de selección, etc.
		self.__oldMousePosition = (0, 0)
		self.__actualMousePosition = (0, 0)

		self.__tileList = []
		for entitytype in entitytypes:
			imageN = wx.Image('images/' + entitytype + 'N.png')
			imageS = wx.Image('images/' + entitytype + 'S.png')
			imageE = wx.Image('images/' + entitytype + 'E.png')
			imageW = wx.Image('images/' + entitytype + 'W.png')
			self.__tileList.append((imageN, imageS, imageE, imageW))
			#image = wx.Image('images/' + entitytype + '.png')
			#self.__tileList.append(image)

		self.palette = []
		for i in range(len(self.colours)):
			pen = wx.Pen(wx.NamedColour(self.colours[i]), 2, wx.SOLID)
			self.palette.append(pen)
		pen = wx.Pen(wx.NamedColour('Blue'), 2, wx.DOT)
		self.palette.append(pen)

		self.__cursors = [wx.StockCursor(wx.CURSOR_ARROW), wx.StockCursor(wx.CURSOR_NO_ENTRY), wx.StockCursor(wx.CURSOR_PENCIL), wx.StockCursor(wx.CURSOR_HAND), wx.StockCursor(wx.CURSOR_SIZING), wx.StockCursor(wx.CURSOR_CROSS)]

		self.SetBackgroundColour('White')
		self.SetCursor(self.__cursors[0])

		self.Bind(wx.EVT_PAINT, self.OnPaint)
		self.Bind(wx.EVT_IDLE, self.OnIdle)
		self.Bind(wx.EVT_SIZE, self.OnSize)

		self.Bind(wx.EVT_MOTION, self.OnMotion)
		self.Bind(wx.EVT_LEFT_UP, self.OnLeftUp)
		self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
		self.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
		self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
		self.Bind(wx.EVT_MIDDLE_UP, self.OnMiddleUp)
		self.Bind(wx.EVT_MIDDLE_DOWN, self.OnMiddleDown)

		self.InitBuffer()

	def CenterMap(self):
		size = self.GetClientSize()
		self.__centerMapPoint = (size[0]/2, size[1]/2)
		self.__displacement = (-1 * ((self.__graphiclevel.getWidth() * self.__zoom) / 2), -1 * ((self.__graphiclevel.getLength() * self.__zoom) / 2))

	def SetZoom(self, value):
		difference = (self.__displacement[0] / self.__zoom, self.__displacement[1] / self.__zoom)
		self.__zoom = value
		self.__displacement = (difference[0] * self.__zoom, difference[1] * self.__zoom)

	def SetNormalMode(self):
		self.__mode = "NORMAL"
		self.SetCursor(self.__cursors[0])
		self.__graphiclevel.setViewGrid(False)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def SetEditMode(self):
		self.__mode = "EDIT"
		self.SetCursor(self.__cursors[1])
		self.__graphiclevel.deselect()
		self.__action = "none"
		self.__oldMousePosition = (0, 0)
		self.__actualMousePosition = (0, 0)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def PaintGrid(self, value):
		self.__paintGrid = value

	def InitBuffer(self):
		size = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(size.width, size.height)
		self.CenterMap()
		dc = wx.BufferedDC(None, self.buffer)
		self.Draw(dc)
		self.reInitBuffer = False

	def Draw(self, dc):
		self.__initMapPoint = (self.__centerMapPoint[0] + self.__displacement[0], self.__centerMapPoint[1] + self.__displacement[1])

		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		dc.BeginDrawing()

		# Dibujo la frontera del nivel
		dc.SetBrush(wx.LIGHT_GREY_BRUSH)
		dc.SetPen(self.palette[0])
		dc.DrawRectangle(self.__initMapPoint[0], self.__initMapPoint[1], self.__graphiclevel.getWidth() * self.__zoom, self.__graphiclevel.getLength() * self.__zoom)

		# Dibujo los tiles
		for entity in self.__graphiclevel.getEntities():
			self.__Paint(entity, dc, self.__initMapPoint[0], self.__initMapPoint[1], self.__zoom, self.__zoom)

		# Dibujo el grid
		if self.__graphiclevel.viewGrid():
			pen = wx.Pen(wx.NamedColour('Yellow'), 2, wx.LONG_DASH)
			dc.SetPen(pen)
			colDisp = 0
			paintLength = self.__graphiclevel.getLength() * self.__zoom
			for col in range(0, self.__graphiclevel.getWidth() + 1):
				dc.DrawLine(self.__initMapPoint[0] + colDisp, self.__initMapPoint[1], self.__initMapPoint[0] + colDisp, self.__initMapPoint[1] + paintLength)
				colDisp += self.__zoom
			rowDisp = 0
			paintWidth = self.__graphiclevel.getWidth() * self.__zoom
			for row in range(0, self.__graphiclevel.getLength() + 1):
				dc.DrawLine(self.__initMapPoint[0], self.__initMapPoint[1] + rowDisp, self.__initMapPoint[0] + paintWidth, self.__initMapPoint[1] + rowDisp)
				rowDisp += self.__zoom

		# Dibujo la selección
		selection = self.__graphiclevel.getSelection()
		if len(selection) > 0:
			#print "Seleccion: ", selection
			initSelectionPoint = (self.__initMapPoint[0] + selection[0][1] * self.__zoom, self.__initMapPoint[1] + selection[0][0] * self.__zoom)
			endSelectionPoint = (self.__initMapPoint[0] + (selection[1][1] + 1) * self.__zoom, self.__initMapPoint[1] + (selection[1][0] + 1) * self.__zoom)
			#print "init: ", initSelectionPoint
			#print "end: ", endSelectionPoint

			pen = wx.Pen(wx.NamedColour('Blue'), 2, wx.LONG_DASH)
			dc.SetPen(pen)
			dc.DrawLine(initSelectionPoint[0], initSelectionPoint[1], initSelectionPoint[0], endSelectionPoint[1])
			dc.DrawLine(initSelectionPoint[0], endSelectionPoint[1], endSelectionPoint[0], endSelectionPoint[1])
			dc.DrawLine(endSelectionPoint[0], endSelectionPoint[1], endSelectionPoint[0], initSelectionPoint[1])
			dc.DrawLine(endSelectionPoint[0], initSelectionPoint[1], initSelectionPoint[0], initSelectionPoint[1])

		# Dibujo el cuadro de obtención de selección
		if self.__paintSelectionBox:
			pen = wx.Pen(wx.NamedColour('Blue'), 2, wx.LONG_DASH)
			dc.SetPen(pen)
			dc.DrawLine(self.__oldMousePosition[0], self.__oldMousePosition[1], self.__oldMousePosition[0], self.__actualMousePosition[1])
			dc.DrawLine(self.__oldMousePosition[0], self.__actualMousePosition[1], self.__actualMousePosition[0], self.__actualMousePosition[1])
			dc.DrawLine(self.__actualMousePosition[0], self.__actualMousePosition[1], self.__actualMousePosition[0], self.__oldMousePosition[1])
			dc.DrawLine(self.__actualMousePosition[0], self.__oldMousePosition[1], self.__oldMousePosition[0], self.__oldMousePosition[1])

		# Dibujo el tile a colocar
		if self.__mode == "EDIT":
			try:
				row, col = self.__GetRowColFromPosition(self.__actualMousePosition)
				startRow, startCol, endRow, endCol = self.__graphiclevel.getBoundingBoxOfEntityToPlace(row, col)
				initPaintPoint = (self.__initMapPoint[0] + startCol * self.__zoom, self.__initMapPoint[1] + startRow * self.__zoom)
				endPaintPoint = (self.__initMapPoint[0] + (endCol + 1) * self.__zoom, self.__initMapPoint[1] + (endRow + 1) * self.__zoom)

				if self.__paintTileBoundingBox:
					pen = wx.Pen(wx.NamedColour('Green'), 2, wx.LONG_DASH)
				else:
					pen = wx.Pen(wx.NamedColour('Red'), 2, wx.LONG_DASH)
				dc.SetPen(pen)
				dc.DrawLine(initPaintPoint[0], initPaintPoint[1], initPaintPoint[0], endPaintPoint[1])
				dc.DrawLine(initPaintPoint[0], endPaintPoint[1], endPaintPoint[0], endPaintPoint[1])
				dc.DrawLine(endPaintPoint[0], endPaintPoint[1], endPaintPoint[0], initPaintPoint[1])
				dc.DrawLine(endPaintPoint[0], initPaintPoint[1], initPaintPoint[0], initPaintPoint[1])
				if self.__graphiclevel.getEntityOrientation() == 'North':
					self.__DrawLetterN(dc, initPaintPoint[0], initPaintPoint[1], self.__zoom, self.__zoom)
				elif self.__graphiclevel.getEntityOrientation() == 'South':
					self.__DrawLetterS(dc, endPaintPoint[0] - self.__zoom, endPaintPoint[1] - self.__zoom, self.__zoom, self.__zoom)
				elif self.__graphiclevel.getEntityOrientation() == 'East':
					self.__DrawLetterE(dc, endPaintPoint[0] - self.__zoom, initPaintPoint[1], self.__zoom, self.__zoom)
				elif self.__graphiclevel.getEntityOrientation() == 'West':
					self.__DrawLetterW(dc, initPaintPoint[0], endPaintPoint[1] - self.__zoom, self.__zoom, self.__zoom)
			except Exception, e:
				#print "Draw: ", e
				pass

		dc.EndDrawing()

	def __GetRowColFromPosition(self, position):
		col = (position[0] - self.__initMapPoint[0]) / self.__zoom
		row = (position[1] - self.__initMapPoint[1]) / self.__zoom
		if col >= 0 and col < self.__graphiclevel.getWidth() and row >= 0 and row < self.__graphiclevel.getLength():
			return row,col
		raise Exception("Out of bounds")

	# Métodos para manejar eventos
	def OnSize(self, event):
		self.reInitBuffer = True

	def OnPaint(self, event):
		dc = wx.BufferedPaintDC(self, self.buffer)
		self.Draw(dc)

	def OnIdle(self, event):
		if self.reInitBuffer:
			self.InitBuffer()
			self.Refresh(False)

	def OnMotion(self, event):
		self.__actualMousePosition = event.GetPositionTuple()
		try:
			row, col = self.__GetRowColFromPosition(self.__actualMousePosition)
			self.__statusbar.PushStatusText("row: " + str(row) + ", col: " + str(col))
		except Exception, e:
			pass
		if self.__action == "selecting":
			dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
			self.Draw(dc)
		elif self.__action == "moving":
			move = (self.__actualMousePosition[0] - self.__oldMousePosition[0], self.__actualMousePosition[1] - self.__oldMousePosition[1])
			#self.__centerMapPoint = (self.__centerMapPoint[0] + move[0], self.__centerMapPoint[1] + move[1])
			self.__displacement = (self.__displacement[0] + move[0], self.__displacement[1] + move[1])
			dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
			self.Draw(dc)
			self.__oldMousePosition = self.__actualMousePosition
		elif self.__action == "painting":
			# Pintar tile del tipo seleccionado
			try:
				row, col = self.__GetRowColFromPosition(self.__actualMousePosition)
				if self.__graphiclevel.setTile(row, col):
					self.SetCursor(self.__cursors[2])
				else:
					self.SetCursor(self.__cursors[1])
				dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
				self.Draw(dc)
			except Exception, e:
				self.SetCursor(self.__cursors[1])
		else:
			if self.__mode == "EDIT":
				try:
					row, col = self.__GetRowColFromPosition(self.__actualMousePosition)
					if self.__graphiclevel.canPlaceTile(row, col):
						#print "Can place entity"
						self.__paintTileBoundingBox = True
						self.SetCursor(self.__cursors[2])
					else:
						self.__paintTileBoundingBox = False
						self.SetCursor(self.__cursors[1])
				except Exception, e:
					#print e
					self.__paintTileBoundingBox = False
					self.SetCursor(self.__cursors[1])
				dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
				self.Draw(dc)

	def OnLeftUp(self, event):
		if self.HasCapture():
			self.ReleaseMouse()
		if self.__mode == "NORMAL":
			#self.__actualMousePosition = event.GetPositionTuple()
			#print "Suelto: ", self.__actualMousePosition
			# Extraer area seleccionada
			try:
				initrow, initcol = self.__GetRowColFromPosition(self.__oldMousePosition)
				endrow, endcol = self.__GetRowColFromPosition(self.__actualMousePosition)
				#print initrow, initcol, endrow, endcol
				tmpinitrow = min(initrow, endrow)
				tmpinitcol = min(initcol, endcol)
				tmpendrow = max(initrow, endrow)
				tmpendcol = max(initcol, endcol)
				#print tmpinitrow, tmpinitcol, tmpendrow, tmpendcol
	
				initrow = max(tmpinitrow, 0)
				initcol = max(tmpinitcol, 0)
				endrow = min(tmpendrow + 1, self.__graphiclevel.getLength())
				endcol = min(tmpendcol + 1, self.__graphiclevel.getWidth())
				#print initrow, initcol, endrow, endcol
				self.__graphiclevel.select(initrow, initcol, endrow - 1, endcol - 1)# En la selecci� hay que quitar una unidad a la casilla de final, porque es justo la que añadimos para que se pinte bien
			except Exception:
				pass

			self.__paintSelectionBox = False
			self.__action = "none"
			self.SetCursor(self.__cursors[0])
		elif self.__mode == "EDIT":
			# Pintar tile del tipo seleccionado
			self.SetCursor(self.__cursors[1])
			self.__action = "none"
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def OnLeftDown(self, event):
		self.CaptureMouse()
		if self.__mode == "NORMAL":
			self.__paintSelectionBox = True
			self.__action = "selecting"
			self.SetCursor(self.__cursors[4])
			self.__oldMousePosition = self.__actualMousePosition
		elif self.__mode == "EDIT":
			self.__action = "painting"
			try:
				row, col = self.__GetRowColFromPosition(self.__actualMousePosition)
				self.__graphiclevel.setTile(row,col)
			except Exception, e:
				#print e
				self.SetCursor(self.__cursors[1])
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def OnRightUp(self, event):
		if self.HasCapture():
			self.ReleaseMouse()
		if self.__mode == "NORMAL":
			self.__graphiclevel.deselect()
			self.__action = "none"
			self.SetCursor(self.__cursors[0])
			self.__actualMousePosition = self.__oldMousePosition
		elif self.__mode == "EDIT":
			pass
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def OnRightDown(self, event):
		self.CaptureMouse()
		if self.__mode == "NORMAL":
			pass
		elif self.__mode == "EDIT":
			self.__graphiclevel.nextEntityOrientation()
			try:
				row, col = self.__GetRowColFromPosition(self.__actualMousePosition)
				if self.__graphiclevel.canPlaceTile(row, col):
					self.__paintTileBoundingBox = True
					self.SetCursor(self.__cursors[2])
				else:
					self.__paintTileBoundingBox = False
					self.SetCursor(self.__cursors[1])
			except Exception, e:
				#print e
				self.__paintTileBoundingBox = False
				self.SetCursor(self.__cursors[1])
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def OnMiddleUp(self, event):
		if self.HasCapture():
			self.ReleaseMouse()
		self.__action = "none"
		self.SetCursor(self.__cursors[0])
		#if self.__mode == "NORMAL":
			#pass
		#elif self.__mode == "EDIT":
			#pass
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def OnMiddleDown(self, event):
		self.CaptureMouse()
		self.__action = "moving"
		self.SetCursor(self.__cursors[5])
		self.__oldMousePosition = event.GetPositionTuple()
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.Draw(dc)

	def Layout(self, event):
		pass

	# Métodos de pintar tiles
	def __Paint(self, entity, dc, mapX, mapY, zoomX, zoomY):
		startRow, startCol, endRow, endCol = self.__graphiclevel.getBoundingBoxOfEntity(entity)

		x = mapX + startCol * zoomX
		y = mapY + startRow * zoomY
		w = (endCol - startCol + 1) * zoomX
		l = (endRow - startRow + 1) * zoomY
		orientationIndex = orientations.index(entity.getOrientation())
		tilesIndex = entitytypes.index(entity.getType())
		#image = self.__tileList[tilesIndex].Scale(w, l)
		#if entity.getOrientation() == 'East':
		#	image = image.Rotate90(False)
		#elif entity.getOrientation() == 'West':
		#	image = image.Rotate90()
		#elif entity.getOrientation() == 'South':
		#	image = image.Rotate90()
		#	image = image.Rotate90()
		#tile = wx.BitmapFromImage(image)
		tile = wx.BitmapFromImage(self.__tileList[tilesIndex][orientationIndex].Scale(w, l))
		dc.DrawBitmap(tile, x, y)

	def __DrawLetterN(self, dc, x, y, w, l):
		dc.SetBrush(wx.WHITE_BRUSH)
		dc.SetPen(self.palette[0])
		wdiv = w / 6
		ldiv = l / 6
		dc.DrawLine(x + wdiv, y + ldiv, x + w - wdiv, y + l - ldiv)
		dc.DrawLine(x + wdiv, y + ldiv, x + wdiv, y + l - ldiv)
		dc.DrawLine(x + w - wdiv, y + ldiv, x + w - wdiv, y + l - ldiv)

	def __DrawLetterS(self, dc, x, y, w, l):
		dc.SetBrush(wx.LIGHT_GREY_BRUSH)
		dc.SetPen(self.palette[0])
		wdiv = w / 6
		ldiv = l / 6
		dc.DrawLine(x + wdiv, y + ldiv, x + w - wdiv, y + ldiv)
		dc.DrawLine(x + wdiv, y + l - ldiv, x + w - wdiv, y + l - ldiv)
		dc.DrawLine(x + wdiv, y + 3 * ldiv, x + w - wdiv, y + 3 * ldiv)
		dc.DrawLine(x + wdiv, y + ldiv, x + wdiv, y + 3 * ldiv)
		dc.DrawLine(x + w - wdiv, y + 3 * ldiv, x + w - wdiv, y + l - ldiv)

	def __DrawLetterE(self, dc, x, y, w, l):
		dc.SetBrush(wx.LIGHT_GREY_BRUSH)
		dc.SetPen(self.palette[0])
		wdiv = w / 6
		ldiv = l / 6
		dc.DrawLine(x + wdiv, y + ldiv, x + wdiv, y + l - ldiv)
		dc.DrawLine(x + wdiv, y + ldiv, x + w - wdiv, y + ldiv)
		dc.DrawLine(x + wdiv, y + l - ldiv, x + w - wdiv, y + l - ldiv)
		dc.DrawLine(x + wdiv, y + 3 * ldiv, x + w - wdiv, y + 3 * ldiv)

	def __DrawLetterW(self, dc, x, y, w, l):
		dc.SetBrush(wx.LIGHT_GREY_BRUSH)
		dc.SetPen(self.palette[0])
		wdiv = w / 6
		ldiv = l / 6
		dc.DrawLine(x + wdiv, y + ldiv, x + 2 * wdiv, y + l - ldiv)
		dc.DrawLine(x + 2 * wdiv, y + l - ldiv, x + 3 * wdiv, y + 3 * ldiv)
		dc.DrawLine(x + 3 * wdiv, y + 3 * ldiv, x + w - 2 * wdiv, y + l - ldiv)
		dc.DrawLine(x + w - 2 * wdiv, y + l - ldiv, x + w - wdiv, y + ldiv)
