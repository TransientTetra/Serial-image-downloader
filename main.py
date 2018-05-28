#!/usr/bin/python2.7

#~~~~~~~~~~~~~HEADER~~~~~~~~~~~~~~~
#This piece of software was written
#and is wholly owned by Mikolaj Sperkowski;
#it cannot be run, published, used, compiled, interpreted,
#edited, copied or shared in any form
#without owner's permission.
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os
import sys
from bs4 import BeautifulSoup
import urllib
import requests
import filecmp
import shutil

#checking for cli arguments
if (len(sys.argv) == 1 or sys.argv[1] == "-h" or sys.argv[1] == "--help"):
	text = "This is a webcomic downloader script, type the website url of the comic you wish to download as a cli parameter\nUsage:\n./main.py [WEBSITE URL]\n./main.py -d/--dir/--directory [DIR TO SAVE] [WEBSITE URL]\nIf you want to know about the version of this program use '-v'"
	print text
elif (sys.argv[1] == "-v" or sys.argv[1] == "--version"):
	text = "Webcomic downloader version 0.4; This piece of software was written by msperkowski it cannot be run, published, used, compiled, interpreted, edited, copied or shared in any form without owner's permission.\nFor more look at msperkowski@github.com"
	print text
else:
	if (sys.argv[1] == "-d" or sys.argv[1] == "--dir" or sys.argv[1] == "directory"):
		dir = sys.argv[2]
		if not os.path.exists(dir):
			print ("Specified directory doesn't exist. Quitting")
		searchedURL = sys.argv[3]
	else:
		#making directory for saved comics
		dir = os.path.dirname(os.path.abspath(__file__))

		#getting website url
		searchedURL = sys.argv[1]

	downloadDirectory = dir +"/comics"
	if not os.path.exists(downloadDirectory):
		os.makedirs(downloadDirectory)
	if not "http" in searchedURL:
		searchedURL = "http://" + searchedURL

	#making websites directory
	currentDirectory = downloadDirectory + '/' + searchedURL.split('/')[2]
	if not os.path.exists(currentDirectory):
		os.makedirs(currentDirectory)


	#main loop
	currentPageNumber = 1;

	while 1:
		currentURL = searchedURL + str(currentPageNumber)
		#here check if exists in folder
		pageDir = currentDirectory + '/' + str(currentPageNumber)
		if os.path.exists(pageDir):
			print (str(currentPageNumber) + " has already been downloaded")
		#checking if given site exists
		elif urllib.urlopen(currentURL).getcode() != 200:
			#checking if current site doesn't exist if the next one exists
			if urllib.urlopen(searchedURL + str(currentPageNumber + 1)).getcode() != 200:
				break
			else:
				currentPageNumber += 1
				continue
		else:
			os.makedirs(pageDir)
			#here downloading
			pageName = searchedURL.split('/')[-2]
			text = "Downloading " + currentURL
			print (text)
			urlResponse = urllib.urlopen(currentURL).read()
			soup = BeautifulSoup(urlResponse, "lxml")
			for image in soup.find_all('img'):
				imageLink =  image.get('src')
				if imageLink != None:
					fileExt = imageLink.split('.')[-1]
					if fileExt == "jpg" or fileExt == "png" or fileExt == "gif":
						if not pageName in imageLink:
							if imageLink[0] == '/':
								if imageLink[1] == '/':
									imageLink = "http:" + imageLink
								else:
									imageLink = "http://" + pageName + imageLink
							else:
								imageLink = "http://" + pageName + '/' + imageLink
						filename = imageLink.split('/')[-1]
						path = os.path.join(pageDir, filename)
						if fileExt == "gif":
							try:
								imageData = requests.get(imageLink).content
							except (UnicodeError, IOError):
								continue
						else:
							try:
								openImage = urllib.urlopen(imageLink)
								imageData = openImage.read()
							except (UnicodeError, IOError):
								continue
						with open (path,"wb") as data:
							data.write(imageData)
			print ("Finished downloading " + currentURL)
		#checking if downloaded page is not the same as previous one
		previousPageDir = currentDirectory + '/' + str(currentPageNumber - 1)
		if os.path.exists(previousPageDir):
			dirCmp = filecmp.dircmp(pageDir, previousPageDir)
			if dirCmp.left_list == dirCmp.right_list:
				shutil.rmtree(pageDir)
				break
		currentPageNumber += 1
				
	print ("Completed downloading from " + searchedURL)
