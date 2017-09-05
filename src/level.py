#!/usr/bin/env python
# -*- coding: utf-8 -*-

from entityfactory import EntityFactory

# Ancho: Width: columnas
# Largo: Length: filas
# Alto: Height:

class Level:
	def __init__(self, name, rows, cols, author = "", id = 1):
		self.__name = name
		self.__author = author
		self.__id = id
		self.__width = cols
		self.__length = rows
		self.__mappingMatrix = [ [None for j in range(self.__width)] for i in range(self.__length) ]
		self.__entityList = []
		self.__rooms = []
		self.__compiled = False
		self.__modified = False
		self.__entitiesIDs = []
		#self.__levelWalls = []# Lista de paredes que pertenecen a la habitación. Su información es correcta al compilar.

	def getName(self):
		return self.__name

	def setName(self, name):
		self.__name = name

	def getID(self):
		return self.__id

	def setID(self, id):
		self.__id = id

	def getWidth(self):
		return self.__width

	def getLength(self):
		return self.__length

	def getEntityAt(self, (row, col)):
		return self.__mappingMatrix[row][col]

	def getEntities(self):
		return self.__entityList[:]

	def getNumberOfEntities(self):
		return len(self.__entityList)

	def getLifts(self):
		lifts = []
		for entity in self.__entityList:
			if entity.getType() == 'Lift':
				lifts.append(entity)
		return lifts

	def __getLiftsCount(self):
		count = 0
		for entity in self.__entityList:
			if entity.getType() == 'Lift':
				count += 1
		return count

	def __getNextEntityID(self):
		if len(self.__entitiesIDs) > 0:
			return self.__entitiesIDs.pop(0)
		else:
			return len(self.__entityList) + 1

	def getModified(self):
		return self.__modified

	def getCompiled(self):
		return self.__compiled

	def getAuthor(self):
		return self.__author

	def setAuthor(self, author):
		self.__author = author

	def __Modify(self):
		self.__modified = True
		self.__compiled = False

	def toCompile(self):
		# Método para comprobar que todo está construido correctamente y para generar las habitaciones
		# TODO
		self.__compiled = False

		# Comprobamos si tiene punto de inicio y Comprobamos si las esquinas estan bien formadas
		hasStartingPoint = 0
		startPoint = None
		for entity in self.__entityList:
			if entity.getType() == 'Start':
				hasStartingPoint += 1
				startPoint = entity

		if hasStartingPoint == 0:
			raise Exception("Level without starting point.")
		elif hasStartingPoint > 1:
			raise Exception("Level with many starting points. Please place just one of them.")
		# Busco paredes en los cuatro sentidos para asegurarme de que estamos dentro
		increments = [[-1,0], [1,0], [0,-1], [0,1]]
		fourWalls = 0
		for inc in increments:
			position = [startPoint.getRowPos(), startPoint.getColPos()]
			while True:
				if position[0] < 0 or position[1] < 0 or position[0] >= self.__length or position[1] >= self.__width:
					raise Exception("Starting point out of room.")
				entity = self.__mappingMatrix[position[0]][position[1]]
				if entity != None:
					if entity.getType() == 'Wall':
						break
				position[0] += inc[0]
				position[1] += inc[1]
		# Si llego aqui es que no ha saltado excepcion, luego hemos encontrado paredes

		# Comienzo con las habitaciones
		self.__findRooms((startPoint.getRowPos(), startPoint.getColPos()))
		#print "Compilación completa. Habitaciones generadas: ", len(self.__rooms)
		self.__compiled = True

	def __findRooms(self, start):
		from room import Room
		neighbours = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]#Lista que nos sirve para la expansión de un tile y buscar los siguientes tiles a explorar
		openTiles = []# Lista de tiles por explorar en una habitación.
		visitedTiles = []# Lista de tiles ya visitados en una habitación.
		visitedWalls = []# Lista de paredes ya visitados en una habitación.
		entitiesInRoom = []# Lista de entidades que se encuentran en una habitación.
		doorsFinded = []# Lista de puertas encontradas en una habitación.
		startingTileInRoom = []# Lista de tiles usados para comenzar la exploración de una habitación

		startingTileInRoom.append(start)
		del self.__rooms[:]
		#del self.__levelWalls[:]

		while (len(startingTileInRoom) > 0):
			del openTiles[:]
			del visitedTiles[:]
			del visitedWalls[:]
			del entitiesInRoom[:]
			del doorsFinded[:]
			initialTileInRoom = startingTileInRoom.pop(0)
			#print "Saco nuevo startTile: ", initialTileInRoom
			revisited = False
			for room in self.__rooms:
				if initialTileInRoom in room.tiles:
					#print "Tile Encontrado. Esta habitación ya ha sido recorrida."
					revisited = True
					break
			if not revisited:
				openTiles.append(initialTileInRoom)
				while (len(openTiles) > 0):
					#print "OpenTiles: ", openTiles
					#print "VisitedTiles: ", visitedTiles
					# Saco el tile de open
					actualTile = openTiles.pop(0)
					# y lo paso el nodo actual a visitados
					visitedTiles.append(actualTile)
					#print "Nuevo tile a expandir en la habitación: ", actualTile
					entity = self.__mappingMatrix[actualTile[0]][actualTile[1]]
					# Guardo la entidad a la que apunta
					if entity != None:
						if entity not in entitiesInRoom:
							#print "Nueva entidad encontrada en la habitación"
							entitiesInRoom.append(entity)
					# Expando el nodo actual si no es una pared
					for neighbour in neighbours:
						expandingTile = (actualTile[0] + neighbour[0], actualTile[1] + neighbour[1])
						if expandingTile[0] < 0 or expandingTile[1] < 0 or expandingTile[0] >= self.__length or expandingTile[1] >= self.__width:
							raise Exception("Map not closed by walls.")
						# Si no está en abiertos ni en visitados o paredes
						if (expandingTile not in openTiles) and (expandingTile not in visitedTiles) and (expandingTile not in visitedWalls) and (expandingTile not in doorsFinded):
							# Es un tile nuevo
							entity = self.__mappingMatrix[expandingTile[0]][expandingTile[1]]
							if entity != None:
								if entity.getType() == 'Door':
									posibleRooms = [[0,-1],[0,1],[-1,0],[1,0]]
									doorPos = (entity.getRowPos(), entity.getColPos())
									for possibleNewRoomTile in posibleRooms:
										tmp = self.__mappingMatrix[doorPos[0] + possibleNewRoomTile[0]][doorPos[1] + possibleNewRoomTile[1]]

										if tmp == None or tmp.getType() != 'Wall':
											#print "Nueva habitacion en ", (doorPos[0] + possibleNewRoomTile[0],doorPos[1] + possibleNewRoomTile[1])
											startingTileInRoom.append((doorPos[0] + possibleNewRoomTile[0],doorPos[1] + possibleNewRoomTile[1]))
									if entity not in doorsFinded:
										doorsFinded.append(entity)
								elif entity.getType() == 'Wall':
									#print "Pared a visitados: ", expandingTile
									# Si es una pared, no querré expandirla, la meto directamente a visitados
									#visitedTiles.append(expandingTile)
									if entity not in visitedWalls:
                                                                            visitedWalls.append(entity)
                                                                            #self.__levelWalls.append(entity)
								else:
									#print "Vecino a expandir: ", expandingTile
									# Meto el tile en abiertos para explorarlo después
									openTiles.append(expandingTile)
							else:
								# Meto el tile en abiertos para explorarlo después
								#print "Vecino a expandir: ", expandingTile
								openTiles.append(expandingTile)
				room = Room(len(self.__rooms) + 1)
				room.tiles = list(visitedTiles)
				room.entities = list(entitiesInRoom)
				room.doors = list(doorsFinded)
				room.walls = list(visitedWalls)
				self.__rooms.append(room)

	def canBePlaced(self, entity, row, col):
		value = True
		try:
			#print "Casilla: (", row, ",", col, "), ", entity.getType()
			width, length, orientation = entity.getWidth(), entity.getLength(), entity.getOrientation()
			startRow, startCol, endRow, endCol = self.getBoundingBox(row, col, entity.getWidth(), entity.getLength(), entity.getOrientation())

			#print "W: ", self.__width, ", L: ", self.__length
			#print "sR: ", startRow, ", sC: ", startCol, ", eR: ", endRow, ", eC: ", endCol
			if startRow < 0 or startCol < 0 or endRow >= self.__length or endCol >= self.__width:
				raise Exception("Try to position entity out of map's bounds.")

			perimeter = self.__getTilesPerimeter(row, col, width, length, orientation)
			#print "Perímetro: ", perimeter
			value = entity.canBePlacedAt(perimeter)
			#print "Valor: ", value
		except Exception, e:
			#print "canBePlaced: ", e
			value = False
		return value

	def placeEntityAt(self, entity, row, col):
		#print "Can be placed:", self.canBePlaced(entity, row, col)
		if self.canBePlaced(entity, row, col):
			# Primero elimino las entidades que ahi hubieran:
			self.eraseEntityAt(row,col)
			#oldentity = self.getEntityAt((row, col))
			#if oldentity != None:
				#startRow, startCol, endRow, endCol = self.getBoundingBox(row, col, oldentity.getWidth(), oldentity.getLength(), oldentity.getOrientation())
				#for x in self.__getTiles(startRow, startCol, endRow, endCol):
					#self.__mappingMatrix[x[0]][x[1]] = None
				#self.__entityList.pop(self.__entityList.index(oldentity))

			# Posiciono la nueva entidad
			entity.setRowPos(row)
			entity.setColPos(col)
			entity.setID(self.__getNextEntityID())

			startRow, startCol, endRow, endCol = self.getBoundingBox(row, col, entity.getWidth(), entity.getLength(), entity.getOrientation())

			for x in self.__getTiles(startRow, startCol, endRow, endCol):
				self.__mappingMatrix[x[0]][x[1]] = entity
			if entity.getType() == 'Lift':
				entity.setLiftID(self.__getLiftsCount() + 1)
			self.__entityList.append(entity)
			self.__Modify()
			return True
		else:
			return False

	def eraseEntityAt(self, row, col):
		entity = self.__mappingMatrix[row][col]
		if entity != None:
			#print "Eliminando entidad en ", row, col
			startRow, startCol, endRow, endCol = self.getBoundingBox(entity.getRowPos(), entity.getColPos(), entity.getWidth(), entity.getLength(), entity.getOrientation())
			
			#print "startRow: ", startRow, ", startCol: ", startCol, ", endRow: ", endRow, ", endCol: ", endCol

			for x in self.__getTiles(startRow, startCol, endRow, endCol):
				self.__mappingMatrix[x[0]][x[1]] = None
			self.__entityList.remove(entity)
			self.__entitiesIDs.append(entity.getID())
			del entity
			self.__Modify()
			return True
		else:
			return False

	def getBoundingBox(self, row, col, width, length, orientation):
		"""Devuelve la lista de indices de la matriz definidos por
			las dimensiones dadas"""

		### ¡¡¡¡¡¡NOTE: La función range(a,b) devuelve los numeros en el intervalo [a,b)!!!!! Para que se tenga en cuenta al calcular los limites startRow, startCol, endRow, endCol
		startRow, startCol, endRow, endCol = row, col, row, col
		if orientation == "North":
			startRow = row
			startCol = col
			endRow = row + length - 1
			endCol = col + width - 1
		elif orientation == "East":
			startRow = row
			startCol = col - length + 1
			endRow = row + width - 1
			endCol = col
		elif orientation == "South":
			startRow = row - length + 1
			startCol = col - width + 1
			endRow = row
			endCol = col
		elif orientation == "West":
			startRow = row - width + 1
			startCol = col
			endRow = row
			endCol = col + length - 1
		else:
			raise Exception( "Invalid orientation" )
		#print "getBoundingBox: w: ", width, ", l: ", length
		#print "getBoundingBox: orientation: ", orientation, ", sR: ", startRow, ", sC: ", startCol, ", eR: ", endRow, ", eC: ", endCol
		return startRow, startCol, endRow, endCol

	def __getTiles(self, startRow, startCol, endRow, endCol):
		"""Devuelve la lista de indices de la matriz definidos por
			las dimensiones dadas"""

		### ¡¡¡¡¡¡NOTE: La función range(a,b) devuelve los numeros en el intervalo [a,b)!!!!! Por eso añadimos un +1 en endRow y endCol para que incluya esos valores.

		tileList = []
		for r in range(startRow, endRow + 1):
			for c in range(startCol, endCol + 1):
				tileList.append((r,c))
		return tileList

	def __getTilesPerimeter(self, row, col, width, length, orientation):
		"""Devuelve la lista de indices del perímetro de la matriz definidos por
			las dimensiones dadas"""
		startRow, startCol, endRow, endCol = self.getBoundingBox(row, col, width, length, orientation)
		#print "perimiter: ", startRow, startCol, endRow, endCol 
		tileList = []
		for i in range(startRow - 1, endRow + 2):
			tmpList = []
			for j in range(startCol - 1, endCol + 2):
				try:
					if i < 0 or j < 0 or i >= self.__length or j >= self.__width:
						tmpList.append('None')
					else:
						entity = self.getEntityAt((i,j))
						tmpList.append(entity.getType())
				except:
					tmpList.append('None')
			tileList.append(tmpList)
		return tileList

	def toXML(self, file, depth = '', levelID = -1):
		if levelID != -1:
			xmlID = levelID
		else:
			xmlID = self.__id
		file.write(depth + '<level id="' + str(xmlID) + '" name="' + self.__name + '"' +
						' length="' + str(self.__length) + '"' +
						' width="' + str(self.__width) + '"' +
						' author="' + str(self.__author) + '"' +
						' rooms_number="' + str(len(self.__rooms)) + '" >\n')
		# Escribo la información de las habitaciones
		file.write(depth + '\t<rooms>\n')
		for room in self.__rooms:
			room.toXML(file, depth + '\t\t')
		file.write(depth + '\t</rooms>\n')
		# Escribo la información de las paredes
		# file.write(depth + '\t<walls>\n')
		#for wall in self.__levelWalls:
		#	wall.toXML(file, depth + '\t\t')
		# file.write(depth + '\t</walls>\n')
		file.write(depth + '</level>\n')

	def fromXML(self, levelDOM):
		from entityfactory import EntityFactory
		factory = EntityFactory()
		self.__name = levelDOM.attributes.getNamedItem('name').value
		self.__length = int(levelDOM.attributes.getNamedItem('length').value)
		self.__width = int(levelDOM.attributes.getNamedItem('width').value)
		self.__author = levelDOM.attributes.getNamedItem('author').value
		self.__mappingMatrix = [ [None for j in range(self.__width)] for i in range(self.__length) ]
		doors = levelDOM.getElementsByTagName('doors')
		for doorDOM in doors:
			for doorChild in doorDOM.childNodes:
				if doorChild.nodeName == 'Door':
					try:
						door = factory.GetNewEntity("Door")
						door.fromXML(doorChild)
						if self.__mappingMatrix[door.getRowPos()][door.getColPos()] == None:
							self.__mappingMatrix[door.getRowPos()][door.getColPos()] = door
							self.__entityList.append(door)
					except:
						pass

		entities = levelDOM.getElementsByTagName('entities')
		for entityDOM in entities:
			for entityChild in entityDOM.childNodes:
				try:
                                    if (entityChild.nodeName == "Slab"):
                                        entity = factory.GetNewEntity(entityChild.nodeName, entityChild.attributes.getNamedItem('type').value)
                                    else:
                                        entity = factory.GetNewEntity(entityChild.nodeName)
				    entity.fromXML(entityChild)
				    startRow, startCol, endRow, endCol = self.getBoundingBox(entity.getRowPos(), entity.getColPos(), entity.getWidth(), entity.getLength(), entity.getOrientation())
				    for x in self.__getTiles(startRow, startCol, endRow, endCol):
                                        self.__mappingMatrix[x[0]][x[1]] = entity
				    self.__entityList.append(entity)
				except:
				    pass

		walls = levelDOM.getElementsByTagName('walls')
		for wallDOM in walls:
			for wallChild in wallDOM.childNodes:
                            if doorChild.nodeName == 'Wall':
				try:
					wall = factory.GetNewEntity("Wall")
					wall.fromXML(wallChild)
					self.__mappingMatrix[wall.getRowPos()][wall.getColPos()] = wall
					self.__entityList.append(wall)
				except:
					pass

		self.__Modify()
