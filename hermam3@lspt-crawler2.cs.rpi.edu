from multiprocessing import Process
import os
import requests 
from bs4 import BeautifulSoup 
import csv


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
def crawl(URL):
	r = requests.get(URL)
	disallowList = crawlRobots(URL)
			
	crawledLinks = []
	soup = BeautifulSoup(r.content, 'html.parser')	
	links = soup.find_all('a')
	text = soup.text()
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
		for links in link:
			if(relevantWord in links):
				return 1
	return 0

if __name__ == '__main__':
	#p = Process(target=child, args(URL))
	#p.start()
	#p.join()
	crawl("https://www.cs.rpi.edu/~goldsd/index.php")
