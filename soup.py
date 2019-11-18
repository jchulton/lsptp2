from multiprocessing import Process
import os
import requests 
from bs4 import BeautifulSoup 
import csv

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

#Input: a string representing the link sent by LA
#		a list of strings representing all links at the given link
#		an int representing the status code returned by querying the webpage
#Output: An int representing the error code, as below:
#		0: Function ran successfully
#		1: Function failed
#Modifies: None
#Send a json string containing a dictionary with the following structure to Link Analysis
#inner-link: https://www.cs.rpi.edu/~goldsd/index.php, status_code: 404, 
#outbond-links: [https://science.rpi.edu/computer-science/programs/undergrad/bs-computerscience],
def LASend(inboundLink, outboundLinks, statusCode):
	return 0

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

#Input: a 

if __name__ == '__main__':
	#p = Process(target=child, args(URL))
	#p.start()
	#p.join()
	crawl("https://www.cs.rpi.edu/~goldsd/index.php")
