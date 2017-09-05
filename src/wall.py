#!/usr/bin/env python
# -*- coding: utf-8 -*-

from entity import Entity

class Wall(Entity):
	def __init__(self, row = 0, col = 0):
		Entity.__init__(self, 'Wall', hSize = 2, rowPos = row, colPos = col)

	def canBePlacedAt(self, perimeter):
		"""
		Una pared no puede situarse si con ello crea paredes de grosor de más de un tile.
		"""
		value = False
		if perimeter[1][1] == "None":
			# Dobles paredes
			if perimeter[0][0] == "Wall" and not ((perimeter[0][1] == "Wall") ^  (perimeter[1][0] == "Wall")):
				value = False
			elif perimeter[0][2] == "Wall" and not ((perimeter[0][1] == "Wall") ^ (perimeter[1][2] == "Wall")):
				value = False
			elif perimeter[2][0] == "Wall" and not ((perimeter[2][1] == "Wall") ^ (perimeter[1][0] == "Wall")):
				value = False
			elif perimeter[2][2] == "Wall" and not ((perimeter[2][1] == "Wall") ^ (perimeter[1][2] == "Wall")):
				value = False
			else:
				value = True

		return value

	def toXML(self, file, depth):
		atrb = str(self.getType()) + ' id="' + str(self.getID()) + '" col="' + str(self.getColPos()) + '" row="' + str(self.getRowPos()) + '"'
		file.write(depth + '<' + atrb + ' />\n')

	def fromXML(self, entityDOM):
		self.setID(int(entityDOM.attributes.getNamedItem('id').value))
		self.setRowPos(int(entityDOM.attributes.getNamedItem('row').value))
		self.setColPos(int(entityDOM.attributes.getNamedItem('col').value))
