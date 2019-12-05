from multiprocessing import Process
import os
import requests 
from bs4 import BeautifulSoup 
import csv
import datetime
from datetime import timedelta
#A list containing all words/phrases that we consider relevant to RPI
RPIRelevantWords = ["RPI", "Renssalaer", "SIS", "Goldschmidt"]


#Input: a string representing the URL 
#Output: None (process terminates)
#Modifies: None
#Given the url, crawl that url using BS4 and send the plaintext, links and updated timestamp to DDS
#def child(URL):

#Input: a string representing the URL 
#Output: a json string containing a dictionary which makes the given pattern (or a None on failure)
	#inner-link: https://www.cs.rpi.edu/~goldsd/index.php, status_code: 404, 
	#outbond-links: [https://science.rpi.edu/computer-science/programs/undergrad/bs-computerscience],
	#last-modified-date: 01-01-0001, plain-text: This is all the plain text not rly tho
#Modifies: Nothing
def crawl(URL, json):
	r = requests.get(URL)
	disallowList = crawlRobots(URL)
			
	crawledLinks = []
	soup = BeautifulSoup(r.content, 'html.parser')	
	links = soup.find_all('a')
	text = soup.getText()
	for link in links:
		linkUrl = link['href']
		linkAllowed = 1
		for disallowedLink in disallowList:
			if(disallowedLink in linkUrl):
				linkAllowed = 0
		if(linkAllowed == 1):
			crawledLinks.append(linkUrl)
	for crawledLink in crawledLinks:
		print(crawledLink)
	print(RPIRelevanceCheck(URL, text ,crawledLinks))
	print(findLastModifiedDate(URL))
	if(RPIRelevanceCheck(URL, text ,crawledLinks) == 1):
		json["inner-link"] = URL
		json["outbond-links"] = crawledLinks
		json["status_code"] = r.status_code
		json["plain-text"] = text
		json["date-to-update"] = findLastModifiedDate(URL)
	else:
		json["inner-link"] = URL
		json["outbond-links"] = []
		json["status_code"] = 600
		json["plain-text"] = None
		json["date-to-update"] = None	

#Input: a string representing the source URL
#Output: a list of all links that are disallowed by robots.txt
#Modifies: nothing
def crawlRobots(URL):
	splitURL = URL.split("/")
	disallowList = []
	robotsLink = splitURL[0]+"/"+splitURL[1]+"/"+splitURL[2] + "/robots.txt"
	f = requests.get(robotsLink)
	for line in f.iter_lines():
		decoded = line.decode()
		if "Disallow:" in decoded:
			DisallowLine = decoded.split("Disallow:")[1].strip()
			disallowList.append(DisallowLine)
	return disallowList
	
#Input: a string representing the source URL
#Output: the last modified date if it can be found, None otherwise
#Modifies: nothing
def findLastModifiedDate(URL):
	splitURL = URL.split("/")
	disallowList = []
	robotsLink = splitURL[0]+"/"+splitURL[1]+"/"+splitURL[2] + "/sitemap.xml"
	f = requests.get(robotsLink)
	soup = BeautifulSoup(f.content, 'lxml')
	surfaceTag = soup.find("loc", string = URL)
	if surfaceTag is None:
		return datetime.datetime.now() + timedelta(days=30)
	changeFreqTag = surfaceTag.find(changefreq)
	lastModTag = surfaceTag.find(lastmod)
	if changeFreqTag is not None:
		changeFreqTagVal = changeFreqTag.getText()
		lastModTagVal = datetime.datetime.strptime(lastModTag.getText(), '%Y-%m-%d')
		if changeFreqTagVal == "weekly":
			return lastModTagVal + timedelta(days=7)
		if changeFreqTagVal == "daily":
			return lastModTagVal + timedelta(days=1)
		if changeFreqTagVal == "monthly":
			return lastModTagVal + timedelta(days=30)
		if changeFreqTagVal == "yearly":
			return lastModTagVal + timedelta(days=365)
		return changeFreqTagVal
	return datetime.datetime.now() + timedelta(days=30)

#Input: a string representing the source URL
# 		a string representing the plaintext
#		list of strings representing the links scraped from the source URL
#Output: a int that represents if the crawled link and plaintext are 'RPI related'. 0: they aren't, 1: the are: -1 error
#Modifies: Nothing
#Loop through the list RPIRelevantWords. If any of these words appaer in the plaintext, source link or scraped links
#The page is RPI relevant. If these words don't appear, it's not. 
def RPIRelevanceCheck(URL, plaintext, links):
	for relevantWord in RPIRelevantWords:
		if(relevantWord in URL):
			return 1
		if(relevantWord in plaintext):
			return 1
		for link in links:
			if(relevantWord in link):
				return 1
	return 0

if __name__ == '__main__':
	#p = Process(target=child, args(URL))
	#p.start()
	#p.join()
	json = dict()
	crawl("https://www.cs.rpi.edu/~goldsd/index.php", json)
	print(json["inner-link"])
	print(json["outbond-links"])
	print(json["status_code"])
	print(json["plain-text"])
	print(json["date-to-update"])
