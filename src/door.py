#!/usr/bin/env python
# -*- coding: utf-8 -*-

from entity import Entity
from entity import orientations

class Door(Entity):
	def __init__(self, row = 0, col = 0, doorOrientation = orientations[0], hidden = False):
		Entity.__init__(self, 'Door', width = 1, hSize = 2, rowPos = row, colPos = col, orientation = doorOrientation)
		self.__hidden = hidden
		self.setPlacingTiles(["Door", "Wall"])

	def canBePlacedAt(self, perimeter):
		value = False
		if perimeter[1][1] == "Wall":
			if self.getOrientation() == "North" or self.getOrientation() == "South":
				if perimeter[0][1] != "Wall" and perimeter[2][1] != "Wall" and perimeter[1][0] == "Wall" and perimeter[1][2] == "Wall":
					value = True
			else:
				if perimeter[0][1] == "Wall" and perimeter[2][1] == "Wall" and perimeter[1][0] != "Wall" and perimeter[1][2] != "Wall":
					value = True

		return value

	def setHidden(self, hidden):
		self.__hidden = hidden

	def getHidden(self):
		return self.__hidden

	def toXML(self, file, depth):
		atrb = str(self.getType()) + ' id="' + str(self.getID()) + '" col="' + str(self.getColPos()) + '" row="' + str(self.getRowPos()) + '" hidden="' + str(self.getHidden()) + '" orientation="' + str(self.getOrientation()) + '"'
		file.write(depth + '<' + atrb + '/>\n')

	def fromXML(self, entityDOM):
		self.setID(int(entityDOM.attributes.getNamedItem('id').value))
		self.setRowPos(int(entityDOM.attributes.getNamedItem('row').value))
		self.setColPos(int(entityDOM.attributes.getNamedItem('col').value))
		self.setHidden(entityDOM.attributes.getNamedItem('hidden').value)
		self.setOrientation(entityDOM.attributes.getNamedItem('orientation').value)
