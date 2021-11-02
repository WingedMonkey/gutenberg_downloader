#!/usr/bin/env python
###############################################################################
# Description:       ITESO MDE, Deep Learning - Project, dataset
# Author:            Alejandro Gutierrez (se705219@iteso.com.mx)
# Version:           0.1
# Usage:             python h5Creator.py
# Python Support:    v3.6.8
###############################################################################

import os.path
import time
import collections

import numpy as np
from pandas import HDFStore
from pandas import DataFrame
import pandas as pd

import random



class bookParser():

	def parseChapter(self, aText, minLen=3000):

		chParragraph=[]

		splitText = aText.split("\n\n\n")
		for text in splitText:
			if len(text) > minLen:
				chParragraph.append(text)

		return chParragraph



class h5Creator():


	def createDataset(self, hdf5_path, booksDir, maxLen, maxChapters):
		
		genres = os.listdir(booksDir)
		filePathList=[]
		genreSampleCounter={}
		for genre in genres:
			if ".txt" not in genre:
				genreDir = os.path.join(booksDir, genre)
				fileList= os.listdir(genreDir)
				genreSampleCounter[genre]=0
				for file in fileList:
					if ".txt" in file:
						fileName = os.path.join(genreDir, file)
						filePathList.append([fileName, genre])





		cp = bookParser()
		hdf5Loader = HDFStore(hdf5_path)


		padding = "".join(["."*maxLen])
		frame = pd.DataFrame({'text':[padding], 'genre':["."]})
		hdf5Loader.append('books', frame)


		dataRows=[]
		for fileName in filePathList:
			f_read = open(fileName[0], "r")
			plainText = f_read.readlines()
			f_read.close()
			for section in cp.parseChapter("".join(plainText)):
				if genreSampleCounter[fileName[1]] <= maxChapters:
					if (len(section) <= maxLen):
						sectionTxt= section
						#print("{0}of{1}".format(len(section), maxLen))
					else:
						sectionTxt= section[:maxLen]

					dataRows.append([sectionTxt, fileName[1]])

					genreSampleCounter[fileName[1]] += 1
					#print("{}".format(genreSampleCounter[genre]))

		random.shuffle(dataRows)
		genreSections=[]
		genreList=[]
		for row in dataRows:
			genreSections.append(row[0])
			genreList.append(row[1])

		for genre in genreSampleCounter:
			print("{}{}".format(genre, genreSampleCounter[genre]))

		testDict= {'text':genreSections, 'genre':genreList}
		frame = pd.DataFrame.from_dict(testDict)
		hdf5Loader.append('books', frame)


		hdf5Loader.close()





class csvCreator():

	def createDataset(self, csv_path, booksDir):
		cp = bookParser()
		csvWriter = open(csv_path, 'a')
		csvWriter.write("genre,text\n")
		genres = os.listdir(booksDir)
		textIndex = 0
		for genre in genres:
			if ".txt" not in genre:
				genreDir = os.path.join(booksDir, genre)
				fileList= os.listdir(genreDir)
				for file in fileList:
					if ".txt" in file:
						fileName = os.path.join(genreDir, file)
						f_read = open(fileName, "r")
						plainText = f_read.readlines()
						f_read.close()
						for chapter in cp.parseChapter("".join(plainText)):
							csvWriter.write("genre_{0},{1}\n".format(genre, chapter))
		csvWriter.close()


	def createDataset(self, hdf5_path, booksDir):
		cp = bookParser()
		hdf5Loader = HDFStore(hdf5_path)
		genres = os.listdir(booksDir)
		textIndex = 0
		for genre in genres:
			if ".txt" not in genre:
				genreDir = os.path.join(booksDir, genre)
				fileList= os.listdir(genreDir)
				for file in fileList:
					if ".txt" in file:
						fileName = os.path.join(genreDir, file)
						f_read = open(fileName, "r")
						plainText = f_read.readlines()
						f_read.close()
						for chapter in cp.parseChapter("".join(plainText)):
							frame = pd.DataFrame({'text':[chapter], 'genre':[genre]}, index=[textIndex])
							hdf5Loader.append('chapters', frame, min_itemsize={'genre':20, 'text': 100000})
							#print("{}-{}-{}".format(textIndex, file, genre))
							textIndex = textIndex +1
		hdf5Loader.close()