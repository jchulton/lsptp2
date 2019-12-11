from flask import Flask, request, current_app
from multiprocessing import Process
import json
import socket
import queue
import time
import importlib
from soup import crawl
app = Flask(__name__)

### API Calls

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
    global q_links
    print("Got LA data")
    link = request.args['link']
    print(link)
    q_links.put(link)

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
LA_url = ""
DDS_url = ""

# queues used to store 
q_links = queue.Queue()
active = []
completed_processes = []
available = 0
limit = 10


### Methods
"""
description: infinite loop which gives new links to our crawling 
    algorithm and replies to LA and DDS
input: none
output: handles processing new links put into q_links then sends the 
    data to LA and DDS
"""
def start_main():
    global app
    with app.app_context():
        
        # only allow at most 10 links to be processed at a time
        global available, limit, q_links, completed_processes, DDS_url, LA_url, need_ack, active

        print("Operating on links")
        time.sleep(3)
        r = request.get('http://127.0.0.1:2500/')

        # this should run forever as the server should never stop
        while r == 200:

            # get recrawl links from DDS
            if time.time() == 0:
                print("Re Crawling links")
                recrawls = request.get(DDS_url, param="/recrawl")
                for link in recrawls:
                    q_links.put(link)
                request.post(DDS_url, param='/ack')
            
            # if a new process space is available, start a new process
            if available < limit and not q_links.empty():
                curr_link = q_links.get(True)
                print("Crawling Link", curr_link)
                json = dict()
                
                # create new process with a reference to a json object (dicitionary)
                pro = Process(target=handle_child, args=(curr_link, json))
                pro.start()
                active.append(pro)
                available += 1
                pro.join()

            # for all active processes, check if they are finished and can be joined
            for pro in active:
                if pro in completed_processes:
                    pro.join()
                    available -= 1


"""
Overview:
Input:
Output:
"""
def handle_child(link, json_object):
    global completed_processes
    
    json_object = crawl(link, json_object)
    print("scraping output", json)  

    # send output to link analysis
    #request.post(LA_url, param={'urls': json['out_links']})
    need_ack = True
    while need_ack:
        continue            
    
    # send JSON object to DDS
    #request.post(DDS_url, param=json)
    need_ack = True
    while need_ack:
        continue

    completed_processes.append(Process.current_process())

if __name__ == "__main__":
    print("Server starting")
    main = Process(target=start_main)
    main.start()
    app.run(host='localhost', port=2500)
    main.join()
