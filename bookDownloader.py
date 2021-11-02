#!/usr/bin/env python
###############################################################################
# Description:       ITESO MDE, Deep Learning - Project, dataset
# Author:            Alejandro Gutierrez (se705219@iteso.com.mx)
# Version:           0.1
# Usage:             python dataSetCreator.py
# Python Support:    v3.6.8
###############################################################################




import os.path
import collections


from gutenbergDownloader.gutenbergDownload import gutenbergDownloader
from gutenbergDownloader.bookgenrestorage import bookGenreStorage
from gutenbergDownloader.h5Creator import h5Creator
from gutenbergDownloader.h5Creator import csvCreator




import sys, getopt

def main(argv):

	MAX_GUTENBERG_ID = 60550
	maxSearchNumber = 1
	if len(argv) > 0:
		reqSearch = int(argv[0])
		if (reqSearch < MAX_GUTENBERG_ID) and (reqSearch > 0):
			maxSearchNumber = reqSearch

	genreKeys = collections.OrderedDict({
		"SciFi": ["cience Fiction", "cience fiction"],
		"Fantasy": ["Fantasy", "fantasy"],
		"Horror": [" horror", "Horror", " Scary", " scary", " terror", "Terror"],
		"Mistery": [" mistery", "Mistery", " detective", " Detective"],
		"Thriller": ["Thriller", " thriller", "Suspense", " suspense"],
		"Adventure": [" adventure", "Adventure"],
		"Romance": ["omance", "omantic"],
		"GenFiction": ["-- Fiction"],
		"Poetry": [" poetry", "Poetry", " poem", "Poem", "Song", " song", " rhyme", "Rhyme", " verses", "Verses"]
		})

	genreOrder = ["SciFi", "Fantasy", "Horror", "Mistery", "Thriller", "Adventure", "Romance", "GenFiction"]
	ctrlFileName = 'bookClasification.txt'
	bookDir = "books"
	myFilito="cache.sqlite"

	sessionCtrlDict= {
		"ctrlFile": ctrlFileName,
		"maxId": MAX_GUTENBERG_ID,
		"waitTime": 15,
		"maxSearch": maxSearchNumber
		}

	downloader = gutenbergDownloader()
	downloader.cachePreloader(myFilito)
	downloader.downloadSession(sessionCtrlDict, genreKeys, bookDir)

	sorter = bookGenreStorage()
	sorter.compressBooks(bookDir)
	sorter.clasifyBooksinDir(ctrlFileName, bookDir, genreKeys.keys())






if __name__ == "__main__":
	main(sys.argv[1:])

