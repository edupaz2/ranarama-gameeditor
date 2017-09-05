#!/usr/bin/env python
# -*- coding: utf-8 -*-

from level import Level
from entity import entitytypes
from entityfactory import EntityFactory

class GraphicLevel:
	def __init__(self, level):
		self.__level = level
		self.__typeOfEntityToPlace = ''
		self.__entityToPlace = None
		self.__entityFactory = EntityFactory()
		self.__viewGrid = False
		self.__selection = []

	def getWidth(self):
		return self.__level.getWidth()

	def getLength(self):
		return self.__level.getLength()

	def getNumberOfEntities(self):
		return self.__level.getNumberOfEntities()

	def getEntities(self):
		return self.__level.getEntities()

	def getSelection(self):
		return self.__selection

	def getTypeOfEntityToPlace(self):
		return self.__typeOfEntityToPlace

	def setTypeOfEntityToPlace(self, value):
		self.__typeOfEntityToPlace = value
		try:
                    if (value.count("Slab") > 0):
			entity = self.__entityFactory.GetNewEntity("Slab", self.__typeOfEntityToPlace)
		    else:
                        entity = self.__entityFactory.GetNewEntity(self.__typeOfEntityToPlace)
                    self.__entityToPlace = entity
		except Exception, e:
		    print "Exception: ", e

	def setViewGrid(self, value):
		self.__viewGrid = value

	def viewGrid(self):
		return self.__viewGrid

	def select(self, initRow, initCol, endRow, endCol):
		del self.__selection[:]
		self.__selection.append((initRow, initCol))
		self.__selection.append((endRow, endCol))

	def deselect(self):
		del self.__selection[:]

	def setTile(self, row, col):
		if self.__entityToPlace != None:
			try:
				#print "setTile en ", row, ", ", col
				if self.__level.placeEntityAt(self.__entityToPlace, row, col):
					self.setTypeOfEntityToPlace(self.__typeOfEntityToPlace)
			except Exception, e:
				#print "setTile: ", e
				pass

	def canPlaceTile(self, row, col):
		value = False
		if self.__entityToPlace != None:
			try:
				value = self.__level.canBePlaced(self.__entityToPlace, row, col)
			except Exception, e:
				#print e
				pass
		return value

	def eraseSelection(self):
		if len(self.__selection):
			initpoint = self.__selection[0]
			endpoint = self.__selection[1]
			
			for row in range(initpoint[0], endpoint[0] + 1):
				for col in range(initpoint[1], endpoint[1] + 1):
					self.__level.eraseEntityAt(row, col)
			self.deselect()
			return True
		return False

	def nextEntityOrientation(self):
		if self.__entityToPlace != None:
			if self.__entityToPlace.getOrientation() == 'North':
				self.__entityToPlace.setOrientation('East')
			elif self.__entityToPlace.getOrientation() == 'East':
				self.__entityToPlace.setOrientation('South')
			elif self.__entityToPlace.getOrientation() == 'South':
				self.__entityToPlace.setOrientation('West')
			else:
				self.__entityToPlace.setOrientation('North')

	def getEntityOrientation(self):
		return self.__entityToPlace.getOrientation()

	def getBoundingBoxOfEntityToPlace(self, row, col):
		if self.__entityToPlace != None:
			orientation = self.__entityToPlace.getOrientation()
			width = self.__entityToPlace.getWidth()
			length = self.__entityToPlace.getLength()
			startRow, startCol, endRow, endCol = self.__level.getBoundingBox(row, col, width, length, orientation)
			return startRow, startCol, endRow, endCol
		else:
			raise Exception("Null entity.")

	def getBoundingBoxOfEntity(self, entity):
		if entity != None:
			startRow, startCol, endRow, endCol = self.__level.getBoundingBox(entity.getRowPos(), entity.getColPos(), entity.getWidth(), entity.getLength(), entity.getOrientation())
			return startRow, startCol, endRow, endCol
		else:
			raise Exception("Null entity.")
