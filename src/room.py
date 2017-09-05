#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Room:
	def __init__(self, roomID):
		self.__id = roomID
		self.tiles = []
		self.doors = []
		self.entities = []
		self.walls = []

	def toXML(self, file, depth):
		atrb = 'id="' + str(self.__id)  + '"'
		file.write(depth + '<room ' + atrb + '>\n')

		# Escribo la información de los tiles de la habitación.
		for tile in self.tiles:
			file.write(depth + '\t<Tile col="' + str(tile[1]) + '" row="' + str(tile[0]) + '" />\n')

		# Escribo la información de las puertas de la habitación.
		file.write(depth + '\t<doors>\n')
		for door in self.doors:
			door.toXML(file, depth + '\t\t')
		file.write(depth + '\t</doors>\n')

		# Escribo la información de las entidades de la habitación.
		file.write(depth + '\t<entities>\n')
		for entity in self.entities:
			entity.toXML(file, depth + '\t\t')
		file.write(depth + '\t</entities>\n')

		# Escribo la información de las paredes de la habitación.
		file.write(depth + '\t<walls>\n')
		for wall in self.walls:
			wall.toXML(file, depth + '\t\t')
		file.write(depth + '\t</walls>\n')

		file.write(depth + '</room>\n')
