#!/usr/bin/env python
# -*- coding: utf-8 -*-
from entity import Entity

''' Enemy Type '''
enemyTypes = ['None', 'PerroInfernal', 'Espectro']

class Generator(Entity):
	def __init__(self, row = 0, col = 0, ratio = 0.0, enemy = enemyTypes[0]):
		Entity.__init__(self, 'Generator', hSize = 2, rowPos = row, colPos = col)

		self.__ratio = ratio
		self.setEnemyType(enemy)

	def setRatio(self, ratio):
		self.__ratio = ratio

	def getRatio(self):
		return self.__ratio

	def setEnemyType(self, enemy):
		if (enemy in enemyTypes):
			self.__enemyType = enemy
		else:
			print '\n__enemyType fuera de rango.'

	def getEnemyType(self):
		return self.__enemyType

	def toXML(self, file, depth):
		atrb = str(self.getType()) + ' id="' + str(self.getID()) + '" row="' + str(self.getRowPos()) + '" col="' + str(self.getColPos()) + '" ratio ="' + str(self.getRatio()) + '" enemyType="' + self.getEnemyType() + '"'
		file.write(depth + '<' + atrb + ' />\n')

	def fromXML(self, entityDOM):
		self.setID(int(entityDOM.attributes.getNamedItem('id').value))
		self.setRowPos(int(entityDOM.attributes.getNamedItem('row').value))
		self.setColPos(int(entityDOM.attributes.getNamedItem('col').value))
		self.setRatio(float(entityDOM.attributes.getNamedItem('ratio').value))
		self.setEnemyType(entityDOM.attributes.getNamedItem('enemyType').value)

