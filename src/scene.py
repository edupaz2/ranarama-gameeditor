#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Scene:
	__maxLevels = 8

	def __init__(self, levels):
		self.__availableLevels = []
		for level in levels:
			if level.getCompiled():
				self.__availableLevels.append(level)

		self.__selectedLevels = []# Los niveles seleccionados

		self.__availableLifts = []
		for level in self.__availableLevels:
			self.__availableLifts.append(level.getLifts())

		self.__selectedLifts = []# Los ascensores seleccionados

		self.__liftsConnections = []

	def GetAvailableLevels(self):
		return self.__availableLevels

	def GetSelectedLevels(self):
		return self.__selectedLevels

	def GetSelectedLifts(self):
		return self.__selectedLifts

	def GetMaxLevels(self):
		return self.__maxLevels

	def GetConnections(self):
		return self.__liftsConnections

	def GetNameOfLevels(self):
		names = []
		for level in self.__availableLevels:
			names.append(level.getName())
		return names

	def SelectLevels(self, levels):
		if len(levels) != self.__maxLevels:
			raise Exception("Invalid levels length.")
		for level in levels:
			#if level not in self.__selectedLevels and level in self.__availableLevels: # Esto evitaría repeticiones
			self.__selectedLevels.append(level)
		# Seleccionamos los ascensores de los niveles seleccionados
		for selectedLevel in self.__selectedLevels:
			index = self.__availableLevels.index(selectedLevel)
			self.__selectedLifts.append(self.__availableLifts[index])

	def SelectLevel(self, levelname):
		if len(self.__selectedLevels) >= self.__maxLevels:
			raise Exception("Can't select more levels.")

		for level in self.__availableLevels:
			if level.getName() == levelname:
				self.__selectedLevels.append(level)
				index = self.__availableLevels.index(level)
				self.__selectedLifts.append(self.__availableLifts[index])
				return

	def SetConnections(self, connections):
		for originLevel, originLift, destinyLevel, destinyLift in connections:
			for connection in self.__liftsConnections:
				if originLevel == connection[0] and originLift == connection[1]:
					raise Exception("Origin Lift already in list.")
			self.__liftsConnections.append((originLevel, originLift, destinyLevel, destinyLift))

	def SetConnection(self, newconnection):
		for connection in self.__liftsConnections:
			if newconnection[0] == connection[0] and newconnection[1] == connection[1]:
				raise Exception("Origin Lift already in list.")
		#print "Añado conexion: ", newconnection
		self.__liftsConnections.append(newconnection)

	def ToXML(self, file):
		# Escribo las conexiones entre ascensores
		# Escribo los niveles
		file.write('<ship>\n')
		file.write('\t<levels>\n')
		levelID = 1
		for level in self.__selectedLevels:
			level.toXML(file, '\t\t', levelID)
			levelID += 1
		file.write('\t</levels>\n')
		file.write('\t<lifts>\n')
		for lift in self.__liftsConnections:
			file.write('\t\t<lift flevel="' + str(lift[0]) + '"  flift="' + str(lift[1]) + '" tlevel="' + str(lift[2]) + '" tlift="' + str(lift[3]) + '" />\n')
		file.write('\t</lifts>\n')
		file.write('</ship>')

	def AreAllLevelsSelected(self):
		return len(self.__selectedLevels) == self.__maxLevels

	def AreAllLiftsSelected(self):
		selectedLifts = 0
		for level in self.__selectedLifts:
			selectedLifts += len(level)
		return selectedLifts == len(self.__liftsConnections)

	def Finalize(self):
		# Metodo que llamamos al final, donde tendremos los niveles seleccionados y las conexiones entre ascensores
		#return self.__selectedLevels, self.__liftsConnections
		pass

