import unittest
from crawler_server import crawl_link
import soup
import datetime


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

    def testCrawlBadResponse(self):
        # BAD RESPONSE, 404 error
        test_url = "https://bleepbloop.com"
        test_json = dict()

        outer_links = []
        code = 404
        text = None
        date = None
        proper_response = make_response(test_url, outer_links, code, text, date)

        soup.crawl(test_url, test_json)
        self.assertDictEqual(test_json, proper_response)
        return

    def testCrawlGoodRelevantResponse(self):
        test_url = "https://sis.rpi.edu"
        test_json = dict()

        outer_links = []
        code = 200
        text = None  # TODO
        date = soup.find_recrawl_date()
        proper_response = make_response(test_url, outer_links, code, text, date)

        soup.crawl(test_url, test_json)
        self.assertDictEqual(test_json, proper_response)
        return

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

    def testCrawlRobots(self):

        url = "file:///home/yev/Desktop/LSP/test_page.html"

        url = "https://science.rpi.edu"

        url = "www.google.com"

        return

    def testRelevance(self):
        # As of now, global variable RPIRelevantWords in soup.py is: ["RPI", "Rensselaer", "SIS"]
        url = "https://testing.com"
        text = "O SIS man, what hath you wrought?"
        links = ["https://dudlink.com"]

        test1 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test1, 1, "Relevance check on text failed.")

        text = "O sis man, what hath you wrought?"
        test2 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test2, 0, "Case-sensitive check on text failed.")

        url = "https://science.rpi.edu"
        test3 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test3, 1, "Relevance check on url given failed.")

        url = "https://test.com"
        links = ["https://rensselaer.com", "https://dudlink.com"]
        test4 = soup.rpi_relevance_check(url, text, links)
        self.assertEqual(test4, 1, "Relevance check on links failed.")
        return


if __name__ == "__main__":
    unittest.main()