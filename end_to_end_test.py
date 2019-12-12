from flask import Flask, request, current_app
from multiprocessing import Process
import sys
import json
import socket
import queue
import time
import requests
import importlib

#creates a mock link analysis server to communicate with crawler server
mock_LA = Flask(__name__)
def send_links(link):
    headers = {'X-API-TOKEN': 'crawl'}
    payload = {'link': link}
    r = requests.post('http://localhost:2500/', data=payload, headers=headers)


# starts the server
if __name__ == "__main__":
    #print("Server starting")
    #mock_LA.run(host='localhost', port=7000)
    #link="https://www.cs.rpi.edu/~goldsd/index.php"
    #send_links(link)      
    #print("Sent 1 link")
    headers = {'X-API-TOKEN': 'crawl'}
    payload = {'link': 'https://www.cs.rpi.edu/~goldsd/index.php'}
    r = requests.post('http://localhost:2500/', data=payload, headers=headers)   
    print(r)