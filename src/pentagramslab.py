#!/usr/bin/env python
# -*- coding: utf-8 -*-

from entity import Entity

class PentagramSlab(Entity):
	def __init__(self, row = 0, col = 0):
		Entity.__init__(self, 'PentagramSlab', rowPos = row, colPos = col)

	def toXML(self, file, depth):
		atrb = str('Slab type="' + self.getType()) + '" id="' + str(self.getID()) + '" col="' + str(self.getColPos()) + '" row="' + str(self.getRowPos()) + '"'
		file.write(depth + '<' + atrb + ' />\n')

	def fromXML(self, entityDOM):
		self.setID(int(entityDOM.attributes.getNamedItem('id').value))
		self.setRowPos(int(entityDOM.attributes.getNamedItem('row').value))
		self.setColPos(int(entityDOM.attributes.getNamedItem('col').value))

