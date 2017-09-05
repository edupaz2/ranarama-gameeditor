#!/usr/bin/env python
# -*- coding: utf-8 -*-

orientations = ['North', 'South', 'East', 'West']

entitytypes = ["None", "Wall", "Door", "Lift", "Generator", "MapSlab", "SaveSlab", "PentagramSlab", "BombSlab", "Table", "Computer", "Container", "Start", "Barrel", "Box", "Closet"]

class Entity:
	def __init__ (self, entityType, width = 1, length = 1, hSize = 0, rowPos = 0, colPos = 0, orientation = orientations[0]):
		self.__setType(entityType)
		self.__id = 0
		self.__width = width
		self.__length = length
		self.__hSize = hSize
		self.__rowPos = rowPos
		self.__colPos = colPos
		self.setOrientation(orientation)
		self.__placingTiles = ["None"]

	def __setType(self, entityType):
		if entityType not in entitytypes:
			raise Exception("Invalid entity type")
		self.__type = entityType

	def getType(self):
		return self.__type

	def setID(self, entID):
		self.__id = entID

	def getID(self):
		return self.__id

	def setWidth(self, width):
		self.__width = width

	def getWidth(self):
		return self.__width

	def setLength(self, length):
		self.__length = length

	def getLength(self):
		return self.__length

	def setHSize (self, altura):
		self.__hSize = altura

	def getHSize (self):
		return self.__hSize

	def setRowPos (self, rowPos):
		self.__rowPos = rowPos

	def getRowPos (self):
		return self.__rowPos

	def setColPos (self, colPos):
		self.__colPos = colPos

	def getColPos (self):
		return self.__colPos

	def getOrientation(self):
		return self.__orientation

	def setOrientation(self, orientation):
		if (orientation in orientations):
			self.__orientation = orientation

	def setPlacingTiles(self, tileList):
		del self.__placingTiles[:]
		self.__placingTiles = tileList

	def getPlacingTiles(self):
		return self.__placingTiles[:]

	def canBePlacedAt(self, perimeter):
		value = True
		#print "Perimeter: ", perimeter
		if self.__orientation == "North" or self.__orientation == "South":
			for r in range(1, self.__length + 1):
				for c in range(1, self.__width + 1):
					entityType = perimeter[r][c]
					value = value and (entityType in self.__placingTiles)
					#print "Evalúo: ", r, ",", c, " ", entityType
		else:
			for r in range(1, self.__width + 1):
				for c in range(1, self.__length + 1):
					entityType = perimeter[r][c]
					value = value and (entityType in self.__placingTiles)
					#print "Evalúo: ", r, ",", c, " ", entityType

		return value

	def toXML(self, file, depth):
		''' Metodo virtual '''
		pass

	def fromXML(self, entityDOM):
		''' Metodo virtual '''
		pass
