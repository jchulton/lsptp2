from flask import Flask
from flask import request
import soup.py
app = Flask(__name__)

# test to see if working properly
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/crawl')
def crawl_link():
    link = request.args.get('url')
    # operate on url
    
    # send output to link analysis
    
    # format JSON object for DDS
    
    # send JSON object to DDS



"""
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