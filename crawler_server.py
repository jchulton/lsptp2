from flask import Flask, request, current_app
from flask_script import Manager
from multiprocessing import Process
import json
import socket
import queue
import time
import requests
import importlib
from soup import crawl
app = Flask(__name__)
manager = Manager(app)

### API Calls

@app.before_first_request
def activate_job():
    #main = Process(target=start_main)
    #main.start()
    #main.join()
    return

"""
Test to see if server is active and responding
"""
@app.route('/helloworld')
def helloworld():
    return "helloworld"

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
"""
@app.route('/ack')
def acknowledgement():
    need_ack = False


### Global Variables

# Boolean variable showing whether an acknowledgement is needed
need_ack = False

# static IP addresses for the Link Analysis and Document Data Store servers
LA_url = "http://lspt-link2.cs.rpi.edu"
DDS_url = ""

# queues used to store 
#q_links = []
#active = []
#completed_processes = []
#available = 0
#limit = 10


### Methods
"""
Overview:
Input:
Output:
"""
def scrape_link(link, json_object):
    
    json_object = crawl(link, json_object)
    print("scraping output", json)

"""
Overview:
Input:
Output:
"""
def send_link_info(json_object):

    # send output to link analysis
    headers = {'X-API-TOKEN': 'return_links'}
    payload = {'link': json_object['inner-link'], 'outgoing': json_object["outbound-links"]}
    #r = requests.post(LA_url, data=payload, headers=headers)
    
    # send JSON object to DDS
    headers = {'X-API-TOKEN': 'crawling_links'}
    #r = requests.post(DDS_url, data=json_object, headers=headers)

    return 1

if __name__ == "__main__":
    print("Server starting")
    app.run(host='localhost', port=2502)
