#!/usr/bin/env python
# -*- coding: utf-8 -*-
import level

class LevelsManager:
	def __init__(self):
		self.__levels = []

	def CreateNewLevel(self, name, numrows, numcols, author):
		# Lanza fuera la excepción Exception
		newlevel = level.Level(name, numrows, numcols, author)
		if not self.__CheckName(name):
			self.__levels.append(newlevel)
			return True
		return False

	def ImportLevelFromFile(self, filename):
		# Lanza fuera la excepción Exception
		newlevel = level.Level("", 0, 0)
		from xml.dom import minidom
		xmldoc = minidom.parse(filename)
		levels = xmldoc.getElementsByTagName('level')
		if len(levels) != 1:
			raise Exception('Needed just one <level> tag in file.')
		newlevel.fromXML(levels[0])
		if not self.__CheckName(newlevel.getName()):
			self.__levels.append(newlevel)
			return True
		return False

	def EraseLevel(self, index):
		level = self.__levels.pop(index)
		del level

	def __CheckName(self, name):
		for level in self.__levels:
			if name == level.getName():
				return True
		return False

	def SaveLevelToFile(self, index, file):
		# Lanza fuera la excepción IndexError
		level = self.__levels[index]
		if not level.getCompiled():
			raise Exception("Level not compiled. You need to compile in order to save it.")
		level.toXML(file)

	def SetLevelName(self, index, name):
		# Lanza fuera la excepción IndexError
		for level in self.__levels:
			if level.getName() == name:
				raise Exception("Level name already exists.")
		self.__levels[index].setName(name)

	def GetLevelName(self, index):
		# Lanza fuera la excepción IndexError
		return self.__levels[index].getName()

	def SetLevelAuthor(self, index, author):
		# Lanza fuera la excepción IndexError
		self.__levels[index].setAuthor(author)

	def GetLevelAuthor(self, index):
		# Lanza fuera la excepción IndexError
		return self.__levels[index].getAuthor()

	#def DuplicateLevel(self, index):
		## Lanza fuera la excepción IndexError
		#copy = self.__levels[index].Duplicate()
		#self.__levels.append(copy)

	def CompileLevel(self, index):
		return self.__levels[index].toCompile()

	def GenerateNewGame(self, levels):
		pass

	def GetListOfLevels(self):
		return self.__levels

	#def GetNamesOfLevels(self):
		#names = []
		#for level in self.__levels:
			#names.append(level.getName())
		#return names

	def GetListOfLifts(self):
		lifts = []
		for level in self.__levels:
			lifts.append(level.getLifts())
		return lifts

	def GetLevel(self, index):
		# Lanza fuera la excepción IndexError
		return self.__levels[index]
