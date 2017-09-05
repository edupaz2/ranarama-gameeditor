#!/usr/bin/env python
# -*- coding: utf-8 -*-

from entity import Entity

class Lift (Entity):
	def __init__ (self, row = 0, col = 0, liftid = 0):
		Entity.__init__(self, 'Lift', rowPos = row, colPos = col)
		self.__id = liftid

	def setLiftID (self, ascID):
		self.__id = ascID

	def getLiftID(self):
		return self.__id

	def toXML(self, file, depth):
		atrb = str(self.getType()) + ' id="' + str(self.getID()) + '" row="' + str(self.getRowPos()) + '" col="' + str(self.getColPos()) + '" liftid="' + str(self.__id) + '"'
		file.write(depth + '<' + atrb +' />\n')

	def fromXML(self, entityDOM):
		self.setID(int(entityDOM.attributes.getNamedItem('id').value))
		self.setRowPos(int(entityDOM.attributes.getNamedItem('row').value))
		self.setColPos(int(entityDOM.attributes.getNamedItem('col').value))
		self.__id = int(entityDOM.attributes.getNamedItem('liftid').value)
