#!/usr/bin/env python
###############################################################################
# Description:       ITESO MDE, Deep Learning - Project, dataset
# Author:            Alejandro Gutierrez (se705219@iteso.com.mx)
# Version:           0.1
# Usage:             python bookgenrestorage.py
# Python Support:    v3.6.8
###############################################################################

import os.path


class bookGenreStorage():

	def compressText(self, aText):
		aText = "".join(aText)
		return aText.replace("\n\n", "\n")


	def compressBooks(self, aDir):
		fileList= os.listdir(aDir)
		for file in fileList:
			if ".txt" in file:
				fileName = os.path.join(aDir, file)
				f_read = open(fileName, "r")
				lines = f_read.readlines()
				f_read.close()
				lines = self.compressText("".join(lines))
				bookWriter = open(fileName, 'w')
				bookWriter.write(lines)
				bookWriter.close()
				print("compressed {0}".format(fileName))


	def clasifyBooksinDir(self, ctrlFileName, aDir, genreKeys):
		if os.path.isfile(ctrlFileName)==True:
			f_read = open(ctrlFileName, "r")
			if f_read != None:
				lines = f_read.readlines()
				f_read.close()
				for line in lines:
					clasifInfo = line.split(" - ")
					if clasifInfo[1] in genreKeys:
						aPath = os.path.join(aDir, clasifInfo[1])
						fileName = "{0}.txt".format(clasifInfo[0])
						srcFileName = os.path.join(aDir, fileName)
						newFilePath = os.path.join(aPath, fileName)
						if os.path.isdir(aPath) != True:
							os.mkdir(aPath)
						if (os.path.isfile(srcFileName)!=False) and (os.path.isfile(newFilePath)==False):
							os.rename(srcFileName, newFilePath)
							print("sorted {0}".format(newFilePath))
