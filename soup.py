from multiprocessing import Process
import os
import requests 
from bs4 import BeautifulSoup 
import csv
import datetime
from datetime import timedelta
#A list containing all words/phrases that we consider relevant to RPI. A webpage with text or links that contains
#One of these words will be considered relevant to RPI. Otherwise, it will be considered not relevant
RPIRelevantWords = ["RPI", "Renssalaer", "SIS"]


#Input: a string representing the URL 
#Output: None
#Modifies: The given dict json. Initially empty, json will be made to match the following pattern
	#inner-link: https://www.cs.rpi.edu/~goldsd/index.php,
	#status-code: 404, 
	#outbond-links: [https://science.rpi.edu/computer-science/programs/undergrad/bs-computerscience],
	#plain-text: This is all the plain text not rly tho,
	#recrawl-date: 01-01-2020
#inner-link: The given URL
#status-code contains the status code that resutls from querying the given URL
#outbound-links: contains all links that are on webpage queried from the given URL
#plain-text: contains all the plaintext that is on the webpage queried from the given URL
#recrawl-date: The date on which the webpage should be recrawled
#If the code fails midway through, the json will not be properly updated and will contain all Nones
#The parent process will know the crawl failed
def crawl(URL, json):
	try:
		
		#If the webpage couldn't be reached, don't try and parse it, just set the status code and return
		r = requests.get(URL)
		if(r.status_code != 200):
			json["inner-link"] = URL
			json["outbond-links"] = []
			json["status-code"] = r.status_code
			json["plain-text"] = None
			json["recrawl-date"] = None
			return	
			
		#Grab the text, disallowed links, and imbedded links from the webpage
		disallowList = crawlRobots(URL)	
		crawledLinks = []
		soup = BeautifulSoup(r.content, 'html.parser')	
		links = soup.find_all('a')
		text = soup.getText()
		
		#Only place non-disallowed links in the list of imbedded links
		for link in links:
			linkUrl = link['href']
			linkAllowed = 1
			for disallowedLink in disallowList:
				if(disallowedLink in linkUrl):
					linkAllowed = 0
			if(linkAllowed == 1):
				crawledLinks.append(linkUrl)
		
		#If the page is RPI relevant, set insert the scraped data into the json
		if(RPIRelevanceCheck(URL, text ,crawledLinks) == 1):
			json["inner-link"] = URL
			json["outbond-links"] = crawledLinks
			json["status-code"] = r.status_code
			json["plain-text"] = text
			json["recrawl-date"] = findRecrawlDate(URL)
			
		#If the page isn't RPI relevant, set the status code to a custom error and don't use the scraped data
		else:
			json["inner-link"] = URL
			json["outbond-links"] = []
			json["status-code"] = 600
			json["plain-text"] = None
			json["recrawl-date"] = None
			
	#If there was a error connecting to the webpage, set the statauts code another custom error	
	except requests.exceptions.ConnectionError:
		json["inner-link"] = URL
		json["outbond-links"] = []
		json["status-code"] = 602
		json["plain-text"] = None
		json["recrawl-date"] = None		

#Input: a string representing the source URL
#Output: a list of all links that are disallowed by robots.txt
#Modifies: nothing
#Transform the given URL into a URL which should lead to the robots.txt file of the webpage, if the roboots.txt exists.
#If robots.txt does exist, parse it for all links that are disallowed. These links will be added to a list and returned.
#If robots.txt does not exist, or if it contains no disallowed links, return an empty list. No links will be disallowed.
#Disallowed links will not be included in the list of inner-links sent to Document Data Storage
def crawlRobots(URL):
	
	splitURL = URL.split("/")
	disallowList = []
	robotsLink = splitURL[0]+"/"+splitURL[1]+"/"+splitURL[2] + "/robots.txt"
	
	#Scrape all the dissallowed links from robots.txt
	f = requests.get(robotsLink)
	for line in f.iter_lines():
		decoded = line.decode()
		if "Disallow:" in decoded:
			DisallowLine = decoded.split("Disallow:")[1].strip()
			disallowList.append(DisallowLine)
	return disallowList
	
#Input: a string representing the source URL
#Output: The date on which the given URL will need to be recrawled
#Modifies: nothing
#Transforms the give URL into a URL which should lead to the sitemap.xml file of the webpage, if the sitemap exists.
#If the sitemap does exist, parse it for the date the webpage was lost modifed at the change frequency.
#Add the change frequency to the last modified date. This is the date on which the webpage will need to be recrawled.
#If the last modified date cannot be found, use the current date. If the change frequency cannot be found, use 1 month.
#If the sitemap doesn't exist, use the defaults above (so return one month later than the current date).
def findRecrawlDate(URL):
#	splitURL = URL.split("/")
#	disallowList = []
#	robotsLink = splitURL[0]+"/"+splitURL[1]+"/"+splitURL[2] + "/sitemap.xml"
#	f = requests.get(robotsLink)
#	soup = BeautifulSoup(f.content, 'lxml')
#	surfaceTag = soup.find("loc", string = URL)
#	if surfaceTag is None:
#		return datetime.datetime.now() + timedelta(days=30)
#	changeFreqTag = surfaceTag.find(changefreq)
#	lastModTag = surfaceTag.find(lastmod)
#	if changeFreqTag is not None:
#		changeFreqTagVal = changeFreqTag.getText()
#		lastModTagVal = datetime.datetime.strptime(lastModTag.getText(), '%Y-%m-%d')
#		if changeFreqTagVal == "weekly":
#			return lastModTagVal + timedelta(days=7)
#		if changeFreqTagVal == "daily":
#			return lastModTagVal + timedelta(days=1)
#		if changeFreqTagVal == "monthly":
#			return lastModTagVal + timedelta(days=30)
#		if changeFreqTagVal == "yearly":
#			return lastModTagVal + timedelta(days=365)
#		return changeFreqTagVal
	return datetime.datetime.now() + timedelta(days=30)

#Input: a string representing the source URL
# 		a string representing the plaintext
#		list of strings representing the links scraped from the source URL
#Output: a int that represents if the crawled link and plaintext are 'RPI related'. 0: they aren't, 1: the are: -1 error
#Modifies: Nothing
#Loop through the list RPIRelevantWords. If any of these words appaer in the plaintext, source link or scraped links
#The page is RPI relevant. If these words don't appear, it's not. non-relevant webpages should not be send to Document Data Storage to be stored.
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
#This main is used for local testing purposes and should be removed/commented out for final implementation
if __name__ == '__main__':
	#p = Process(target=child, args(URL))
	#p.start()
	#p.join()
	json = dict()
	crawl("https://www.cs.rpi", json)
	print(json["inner-link"])
	print(json["outbond-links"])
	print(json["status-code"])
	print(json["plain-text"])
	print(json["recrawl-date"])
