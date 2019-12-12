import unittest
import soup
import datetime

# Input: a dict representing an empty json file
#   link: The given URL
#   code: contains the status code that results from querying the given URL
#   outer_links: contains all links that are on webpage queried from the given URL
#   text: contains all the plaintext that is on the webpage queried from the given URL
#   date: The date on which the webpage should be recrawled
# Output: A dict representing a json file that would be sent to Document Data storage
# Modifies: None
# Given all needed information, parse that needed information into dict that can turned into a json file
def make_response(link, outer_links, code, text, date):
    proper_json = dict()
    proper_json["inner-link"] = link
    proper_json["outbound-links"] = outer_links
    proper_json["status-code"] = code
    proper_json["plain-text"] = text
    proper_json["recrawl-date"] = date
    return proper_json


# These tests are meant to test all edge-cases and branches of crawler_server.py and soup.py
class TestEdges(unittest.TestCase):
    @staticmethod
    def findRecrawlDate():
        new_time = soup.find_recrawl_date()
        if isinstance(new_time, datetime.datetime):
            return
        raise ValueError("new_time found does not follow datetime standard.")

    #Ensure that passing a non existing link to crawl results in a 404 being returned
    def testCrawlBadResponse(self):
        # BAD RESPONSE, 404 error
        test_url = "http://paper.com/users"
        test_json = dict()

        outer_links = []
        code = 404
        text = None
        date = None
        proper_response = make_response(test_url, outer_links, code, text, date)

        soup.crawl(test_url, test_json)
        self.assertDictEqual(test_json, proper_response)
        return

    #Ensure that passing a valid, rpi relevant link to crawl results in the data that was hand scraped from the web page
    def testCrawlGoodRelevantResponse(self):
        test_url = "https://science.rpi.edu/"
        test_json = dict()

        outer_links = []
        code = 200
        text = None
        date = soup.find_recrawl_date()
        proper_response = make_response(test_url, outer_links, code, text, date)

        soup.crawl(test_url, test_json)
        self.assertNotEqual(sorted(test_json['outbound-links']), sorted(proper_response['outbound-links']))
        self.assertIsNotNone(test_json['plain-text'])
        return

    #Ensure that passing a valid, not rpi relevant link to crawl results in a 600 error
    def testCrawlGoodIrrelevantResponse(self):
        # GOOD RESPONSE, NO RPI RELEVANCE, 600 error
        test_url = "https://onebananas.com/"
        test_json = dict()

        outer_links = []
        code = 600
        text = None
        date = None
        proper_response = make_response(test_url, outer_links, code, text, date)

        soup.crawl(test_url, test_json)
        self.assertDictEqual(test_json, proper_response)
        return

    #Ensure that passing a malformed link to crawl results in a 602 error
    def testCrawlNoResponse(self):
        # NO CONNECTION RESPONSE, 602 error
        test_url = "https://test"
        test_json = dict()

        outer_links = []
        code = 602
        text = None
        date = None
        proper_response = make_response(test_url, outer_links, code, text, date)

        soup.crawl(test_url, test_json)
        self.assertDictEqual(test_json, proper_response)
        return

    #Test the crawl_robots function when a url has a robots.txt and doesn't have a robots.txt
    def testCrawlRobots(self):

        #No robots.txt is the link below, crawl_robots should be an empty link
        url = "http://blog.davidstea.com/robots.txt"
        disallow_list = soup.crawl_robots(url)
        self.assertEqual(disallow_list, [])

        #There is valid robots.txt at the link below, which contains dissallowed links.
        #Make sure that the disallowed links are scraped and removed during the crawl process
        url = "https://science.rpi.edu"
        disallow_list = soup.crawl_robots(url)
        self.assertNotEqual(disallow_list, [])
        server_response = dict()
        soup.crawl(url, server_response)
        for unallowed_link in disallow_list:
            for link in server_response['outbound-links']:
                self.assertNotIn(unallowed_link, link)

        #No robots.txt is the link below, crawl_robots should be an empty link
        url = "www.google.com"
        disallow_list = soup.crawl_robots(url)
        self.assertEqual(disallow_list, [])

        return

    #Test the rpi_relevance_check function when pages are and aren't rpi relevant
    def testRelevance(self):
        
        #Check that relevant text is noticed
        url = "https://testing.com"
        text = "O SIS man, what hath you wrought?"
        links = ["https://dudlink.com"]

        test1 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test1, 1, "Relevance check on text failed.")

        #Check that rpi_relevance_check matching is case insensitive
        text = "O sis man, what hath you wrought?"
        test2 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test2, 1, "Case-insensitive check on text failed.")

        #Check that relevant url is noticed
        text = "I'm not relevant ):"
        url = "https://science.rpi.edu"
        test3 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test3, 1, "Relevance check on url given failed.")

        #Check that relevant link is noticed
        url = "https://test.com"
        links = ["https://rensselaer.com", "https://dudlink.com"]
        test4 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test4, 1, "Relevance check on links failed.")
        return
        
        #Check that a page is non relevant when no releated words are found
        links = ["https://notrelevant.gov"]
        test4 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test4, 0, "Non relevance check failed.")
        return


if __name__ == "__main__":
    unittest.main()
