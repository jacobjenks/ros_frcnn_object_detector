#!/usr/bin/env python
import json

class Object:
	'''
	This class contains the definitions of the objects we are searching for
	'''
	classes = [] # Static list of classes we're looking for
	objects = [] # Static list of objects we're looking for
	num_classes = 0

	def __init__(self, classID, objectID, width, height, color):
		self.classID = classID
		self.objectID = objectID
		self.width = width 
		self.height = height
		self.color = color

	@staticmethod
	def initDefinitions():
		with open("objects.json") as data:
			data = json.load(data)
		for c in data["classes"]:
			Object.classes.append(c)
	
		Object.num_classes = len(Object.classes)

		i = 0
		for obj in data["objects"]:
			Object.objects.append(Object(Object.classes.index(obj["class"]), i, obj["width"], obj["height"], obj["color"]))
			i++
	
	@staticmethod
	def getObject(classID, color):
		objects = []
		for obj in Objects.objects:
			if obj.classID == classID:
				objects.append(obj)

		if len(objects) == 1:
			return objects[0]
		else:
			#get object with nearest color
			closest = objects[0]
			distance = 999999
			for obj in objects:
				d = Object.colorDistance(obj.color, color)
				if d < distance:
					closest = obj
					distance = d

			return closest
			
	def getColorDistance(c1, c2):
		# Get euclidean distance between two colors
		# I'm sure there's a better way to do this
		return math.sqrt(math.pow(c1[0] - c2[0], 2) + math.pow(c1[1] - c2[1], 2) + math.pow(c1[2] - c2[2]))
			

	def name(self, classID = -1):
		if classID == -1:
			classID = self.classID
		return classNames[classID]


class ObjectDetection:
	'''
	This class is a container for info pertaining to a detection event for an object
	'''
	#This is the number of pixels for an object 1 meter wide at a distance of 1 meter for our particular webcam
	pixelRatio = 1280

	def __init__(self, classID, xMin, yMin, xMax, yMax, confidence, color):
		self.classID = classID
		self.obj = Object.getObject(classID, color)
		self.xMin = xMin
		self.yMin = yMin
		self.xMax = xMax
		self.yMax = yMax
		self.confidence = confidence
		self.color = color

	#Estimate the distance to an object using its angular diameter (in pixels),
	# and a pixel ratio calibrated for our specific camera
	def distance(self, yMin = -1, yMax = -1):
		yMin = self.yMin if yMin == -1 else yMin
		yMax = self.yMax if yMax == -1 else yMax
		return self.pixelRatio/self.height/(yMax - yMin)

##########################

Object.initDefinitions()
