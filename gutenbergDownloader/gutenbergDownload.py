#!/usr/bin/env python
###############################################################################
# Description:       ITESO MDE, Deep Learning - Project, dataset
# Author:            Alejandro Gutierrez (se705219@iteso.com.mx)
# Version:           0.1
# Usage:             python gutenbergDownload.py
# Python Support:    v3.6.8
###############################################################################


from gutenberg.acquire import load_etext
from gutenberg.cleanup import strip_headers
from unidecode import unidecode
from gutenberg.query import get_etexts
from gutenberg.query import get_metadata
from gutenberg.query import list_supported_metadatas
from gutenberg.acquire import set_metadata_cache
from gutenberg.acquire.metadata import SqliteMetadataCache
import os.path
import time
import collections



meta = ['author', 'formaturi', 'language', 'rights', 'subject', 'title']


class gutenbergDownloader():

	def cachePreloader(self, cacheFile):
		cache = SqliteMetadataCache(cacheFile)
		if os.path.isfile(cacheFile)!=True:
			cache.populate()
		else:
			print("cache downloaded")
		set_metadata_cache(cache)


	def isTxtAvailable(self, id):
		formatUri = get_metadata('formaturi', id)
		for fileFormat in formatUri:
			if ".txt" in fileFormat:
				return True
		return False


	def isEnglish(self, id):
		englishBook = False
		language = get_metadata('language', id)
		if 'en' in language:
			englishBook = True
		return englishBook


	def isGenre(self, bookGenre, bookSubjects):
		for bookSubject in bookSubjects:
			for substr in bookGenre:
				if substr in bookSubject:
					return True
		return False


	def matchGenre(self, genreKeys, bookSubjects):
		for aGenre in genreKeys.keys():
			if self.isGenre(genreKeys[aGenre], bookSubjects)==True:
				return aGenre
		return None


	def downloadBook(self, id, aPath):
		success = False
		try:
			bookText = strip_headers(load_etext(id)).strip()
		except: # catch *all* exceptions
			bookText = None

		if bookText != None:
			strs = unidecode(bookText)
			fileName = os.path.join(aPath, "{0}.txt".format(id))
			bookWriter = open(fileName, 'w')
			bookWriter.write(strs)
			bookWriter.close()
			success = True

		return success


	def getAllEnglishBooks(self):
		englishBooks = get_etexts('language', 'en')
		fileName = "englishBooksList.txt"
		listWriter = open(fileName, 'w')
		for bookId in englishBooks:
			strs = unidecode(bookId)
			listWriter.write("{0}\n".format(strs))
		listWriter.close()
		return fileName


	def resumeNumber(self, ctrlFileName):
		resume = 0
		if os.path.isfile(ctrlFileName)==True:
			f_read = open(ctrlFileName, "r")
			if f_read != None:
				lines = f_read.readlines()
				f_read.close()
				if len(lines)>0:
					last_line = lines[-1]
					resume = int((last_line.split(" - "))[0])+1
		return resume


	def getSubject(self, id):
		return get_metadata('subject', id)


	def getTitle(self, id):
		return get_metadata('title', id)


	def downloadSession(self, sessionCtrlDict, genreKeys, bookDir="boks"):
		print("Looking for english books available in txt format, matching subgenre list for fiction")

		bookWriter = open(sessionCtrlDict["ctrlFile"], 'a')
		sessionCounter = 0

		for id in range(self.resumeNumber(sessionCtrlDict["ctrlFile"]), sessionCtrlDict["maxId"]):
			time.sleep(sessionCtrlDict["waitTime"])
			#verify book is available in txt format
			clasification = ""
			if self.isTxtAvailable(id)==True:
				#verify book subject matches our search
				bookSubjects = self.getSubject(id)
				if self.isGenre(genreKeys["Poetry"], bookSubjects)==False:
					genre = self.matchGenre(genreKeys, bookSubjects)
					if genre != None:
						if self.isEnglish(id) == True:
							if self.downloadBook(id, bookDir) != False:
								clasification = "{0} - {1} - {2}".format(id, genre, self.getTitle(id))
							else:
								clasification = "{0} - Download failed".format(id)
						else:
							clasification = "{0} - Not in English".format(id)
					else:
						clasification = "{0} - Not fiction subgenre match".format(id, genre)
				else:
					clasification = "{0} - Poetry not wanted".format(id)
			else:
				clasification = "{0} - No txt available".format(id)

			bookWriter.write("{0}\n".format(unidecode(clasification)))
			print(clasification)
			sessionCounter = sessionCounter + 1

			if sessionCounter >= sessionCtrlDict["maxSearch"]:
				break

		bookWriter.close()

