from flask import Flask
from flask import request
import json
import soup.py as crawler
import time
app = Flask(__name__)

LA_url = ""
DDS_url = ""

# test to see if working properly
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/crawl')
def crawl_link():
    link = request.args.get('url')
    # operate on url
    crawler_output = crawler.crawl(link)
    # send output to link analysis
    request.post(LA_url, param={'urls': outgoing_links})
    # format JSON object for DDS
    DDS_output = dict()
    DDS_output["link"] = link
    DDS_output["status"] = crawler_output["status"] # will crawler return this???
    DDS_output["text"] = "" # are we not giving the raw html anymore???
    DDS_output["crawled_links"] = crawler_output[outgoing_links]
    DDS_output["last_updated_date"] = time.ctime()
    # send JSON object to DDS
    request.post(LA_url, param=DDS_output)


"""
NEED TO DO:
send ACK to LA when we get input
wait for ACK from DDS, and decide what to do if we don't recieve one in x time
get info on how to connect with LA and DDS servers
refine when/how recrawling will take place
format with codeing style specifications


JSON format:
'{ 
"link":"https://www.cs.rpi.edu/~goldsd/index.php", 
"status":200, 
"text":"I am all the text on the page (no I’m not but putting all the text would make this very messy)",
"crawled_links": [], 
"last_updated_date":""
}'


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