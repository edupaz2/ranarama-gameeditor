#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wall import Wall
from door import Door
from lift import Lift
from generator import Generator
from mapslab import MapSlab
from saveslab import SaveSlab
from pentagramslab import PentagramSlab
from bombslab import BombSlab
from startposition import StartPosition
from obstacle import Obstacle

class EntityFactory:
	def __init__(self):
		pass

	def GetNewEntity(self, entitytype, entitySubtype = ""):
		entity = None
		if (entitytype == "Wall"):
                    entity = Wall()
		elif (entitytype == "Door"):
                    entity = Door()
		elif (entitytype == "Lift"):
                    entity = Lift()
		elif (entitytype == "Generator"):
                    entity = Generator()
		elif (entitytype == "Slab"):
                    if (entitySubtype == "MapSlab"):
        		entity = MapSlab()
        	    elif (entitySubtype == "SaveSlab"):
			entity = SaveSlab()
        	    elif (entitySubtype == "PentagramSlab"):
                        entity = PentagramSlab()
                    elif (entitySubtype == "BombSlab"):
                        entity = BombSlab()
		elif (entitytype == "Table"):
			entity = Obstacle(obstacleType = "Table", width = 2, length = 1)
		elif (entitytype == "Computer"):
			entity = Obstacle(obstacleType = "Computer", width = 3, length = 1)
		elif (entitytype == "Container"):
			entity = Obstacle(obstacleType = "Container", width = 1, length = 1)
		elif (entitytype == "Start"):
			entity = StartPosition()
		elif (entitytype == "Barrel"):
			entity = Obstacle(obstacleType = "Barrel", width = 1, length = 1)
		elif (entitytype == "Box"):
			entity = Obstacle(obstacleType = "Box", width = 1, length = 1)
		elif (entitytype == "Closet"):
			entity = Obstacle(obstacleType = "Closet", width = 1, length = 1)
		else:
			raise Exception("Invalid type: " + entitytype)
		return entity

