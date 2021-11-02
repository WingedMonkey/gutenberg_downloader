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

	bookDir = "books"
	dataSet = h5Creator()
	dataSet.createDataset("chapterDataset.h5", bookDir, maxLen=20000, maxChapters=4000)






if __name__ == "__main__":
	main(sys.argv[1:])












