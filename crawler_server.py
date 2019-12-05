from flask import Flask, request
from multiprocessing import Process
import json
import queue
import time
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
@app.route('/crawl')
def crawl_link():
    link = request.args.get('url')
    q.put(link)
    # send output to link analysis
    request.post(LA_url, param='/ack')


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
LA_url = ""
DDS_url = ""

# queues used to store 
q_links = queue.Queue()
q_active = queue.Queue()

# only allow at most 10 links to be processed at a time
available = 0
limit = 10

### Methods

"""
description: infinite loop which gives new links to our crawling algorithm and replies to LA and DDS
input: none
output: handles processing new links put into q_links then sends the data to LA and DDS
"""
def start_main():
    # this should run forever as the server should never stop
    while True:
        
        # get recrawl links from DDS
        if time.time() == 0:
            recrawls = request.get(DDS_url, param="/recrawl")
            for link in recrawls:
                q_links.put(link)
            request.post(DDS_url, param='/ack')
        
        # if a new process space is available, start a new process
        if available < limit and not q_links.empty():
            json = dict()
            
            # create new process with a reference to a json object (dicitionary)
            pro = Process(target=crawl(), args=(q_links.get(True), json))
            q_active.put((json, pro))
            available += 1
            pro.start()
        
        # if a process is running, join it and send the output to LA and DDS
        if not q_active.empty():
            json, pro = q_active.get(True)
            pro.join()
            
            # send output to link analysis
            request.post(LA_url, param={'urls': json['out_links']})
            need_ack = True
            while need_ack:
                continue            
            
            # send JSON object to DDS
            request.post(DDS_url, param=json)
            need_ack = True
            while need_ack:
                continue            
            available -= 1    

"""
Description: starts main loop
"""
if __name__ == "__main__":
    start_main()
            





"""
NEED TO DO:
X send ACK to LA when we get input
wait for ACK from DDS, and decide what to do if we don't recieve one in x time
get info on how to connect with LA and DDS servers
refine when/how recrawling will take place
format with codeing style specifications


Document Data Store:
PUSHING
    DELETE request:
        if we find a url that should not be a search result
        do we still send a full json object or just the url???
    PUT request: COMPLETED
        if we find a url that should be searched send json object
PULLING
    GET request: COMPLETED????
        if we need to recrawl a url????

Link Analysis:
TAKE
    /crawl url: COMPLETED
        operate on incoming link
SEND
    POST request: COMPLETED
        send outgoign urls
"""