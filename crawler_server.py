from flask import Flask
from flask import request
from multiprocessing import Process
import json
import queue
import time
import importlib
Crawl = importlib.import_module("soup.py")
app = Flask(__name__)

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
    request.post(LA_url, param='ack')

#@app.route('/ack')
#def acknowledgement():
#    return

"""
Description: Main loop method, handles a queue of links and passes them onto our crawling algoirthm
"""
if __name__ == "__main__":
    
    # static IP addresses for the Link Analysis and Document Data Store servers
    LA_url = ""
    DDS_url = ""
    
    # queues used to store 
    q_links = queue.Queue()
    q_active = queue.Queue()
    
    # only allow at most 10 links to be processed at a time
    available = 0
    limit = 10
    
    # this should run forever as the server should never stop
    while True:
        
        # if a new process space is available, start a new process
        if available < limit and not q_links.empty():
            json = dict()
            
            # create new process with a reference to a json object (dicitionary)
            pro = Process(target=Crawl.crawl(), args=(q_links.get(True), json))
            q_active.put((json, pro))
            available += 1
            pro.start()
        
        # if a process is running, join it and send the output to LA and DDS
        if not q_active.empty():
            json, pro = q_active.get(True)
            pro.join()
            
            # send output to link analysis
            request.post(LA_url, param={'urls': json['out_links']})
            
            # send JSON object to DDS
            request.post(DDS_url, param=json)
            available -= 1
            

"""
NEED TO DO:
send ACK to LA when we get input
wait for ACK from DDS, and decide what to do if we don't recieve one in x time
get info on how to connect with LA and DDS servers
refine when/how recrawling will take place
format with codeing style specifications


Document Data Store:
PUSHING
    DELETE request:
        if we find a url that should not be a search result
        do we still send a full json object or just the url???
    PUT request:
        if we find a url that should be searched send json object
PULLING
    GET request:
        if we need to recrawl a url????

Link Analysis:
TAKE
    /crawl url:
        operate on incoming link
SEND
    POST request:
        send outgoign urls
"""