from flask import Flask, request, current_app
from multiprocessing import Process
import sys
import json
import socket
import queue
import time
import requests
import importlib
from soup import crawl
app = Flask(__name__)

### API Calls
"""
Description: Takes a /crawl request from L.A. and queues a new link
Input: A crawl request with a single link (string) as a parameter
Output: Sends the link to a queue of urls which will be processed.
        Also sends an acknowledgment to LA
Effects: queues a new link to q_links
"""
@app.route('/crawl', methods=['POST'])
def crawl_link():
    link = request.args['link']
    json_object = dict()
    scrape_link(link, json_object)
    send_link_info(json_object)
    print(link, json_object)
    # send output to link analysis
    return 'ack'


"""
Description: Recognize if an acknowledgement was recieved
Input: An /ack request
Effects: tells the server another componenet has recieved our data
Modifies: nothing
"""
@app.route('/ack')
def acknowledgement():
    need_ack = False


### Global Variables
# Boolean variable showing whether an acknowledgement is needed
need_ack = False

# static IP addresses for the Link Analysis and Document Data Store servers
LA_url = sys.argv[2]
DDS_url = sys.argv[3]

### Methods
"""
Overview: Using the crawling algorithm, process the link and scrape the data from it
Input: string - link, dictionary - json object
Output: the reference object 'json_object' will store all data gathered during the crawling into said object
Modifies: nothing
"""
def scrape_link(link, json_object):
    # call the crawl algorithm on the given link
    json_object = crawl(link, json_object)

"""
Overview: Send the gathered JSON object to DDS, and portions of it to LA
Input: dictionary - json_object holding all pertinent information
Output: None
Effects: Sends data to both DDS and LA for them to store and manipulate, respectively 
"""
def send_link_info(json_object):

    # send output to link analysis
    headers = {'X-API-TOKEN': 'return_links'}
    payload = {'link': json_object['inner-link'], 'outgoing': json_object["outbound-links"]}
    r1 = requests.post(LA_url, data=payload, headers=headers)
    
    # send JSON object to DDS
    headers = {'X-API-TOKEN': 'crawling_links'}

    # depending on what is gotten from this request, send a put/post request with the JSON object to DDS
    if(requests.get(DDS_url, data={'link': json_object['inner-link']}, headers={'X-API-TOKEN': 'link'})):
        r2 = requests.put(DDS_url, data=json_object, headers=headers)
    else:
        r2 = requests.post(DDS_url, data=json_object, headers=headers)


# Starts the server
if __name__ == "__main__":
    print("Server starting")
    app.run(host='localhost', port=int(sys.argv[1]))
