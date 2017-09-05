#!/usr/bin/env python
# -*- coding: utf-8 -*-

from entity import Entity
from entity import orientations

class Obstacle(Entity):
	#obstaclesTypes = ["Table", "Computer", "Machine", "Container"] # Tienen que coincidir con los de entity.entitytypes

	def __init__(self, obstacleType = "Table", row = 0, col = 0, width = 3, length = 2, obsOrientation = orientations[0]):
		#self.setObstacleType(obstacleType)
		Entity.__init__(self, obstacleType, width, length, hSize = 1, rowPos = row, colPos = col, orientation = obsOrientation)

	#def setObstacleType(self, obstacleType):
		#if obstacleType not in self.obstaclesTypes:
			#raise Exception("Type not allowed.")
		#self.__obstacleType = obstacleType

	def toXML(self, file, depth):
		atrb = 'type="' + str(self.getType()) + '" id="' + str(self.getID()) + '" row="' + str(self.getRowPos()) + '" col="' + str(self.getColPos()) + '" width="' + str(self.getWidth()) + '" length="' + str(self.getLength()) + '" orientation="' + self.getOrientation() + '"'# obstacletype="' + str(self.__obstacleType) + '"'
		file.write(depth + '<Obstacle ' + atrb + ' />\n')

	def fromXML(self, entityDOM):
		self.setID(int(entityDOM.attributes.getNamedItem('id').value))
		self.setRowPos(int(entityDOM.attributes.getNamedItem('row').value))
		self.setColPos(int(entityDOM.attributes.getNamedItem('col').value))
		self.setWidth(int(entityDOM.attributes.getNamedItem('width').value))
		self.setLength(int(entityDOM.attributes.getNamedItem('length').value))
		self.setOrientation(entityDOM.attributes.getNamedItem('orientation').value)
