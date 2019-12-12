
import unittest
from crawler_server import crawl_link
import soup.py

class TestCrawlLink(unittest.TestCase):
    
    def no_violations_no_sitemap(self):
        proper_response = ""  # TODO: Create proper JSON response
        self.assertEqual(crawl_link(), proper_response)
        return

    def no_violations_yes_sitemap(self):
        proper_response = ""  # TODO: Create proper JSON response
        self.assertEqual(crawl_link(), proper_response)
        return

    def yes_violations_no_sitemap(self):
        proper_response = ""  # TODO: Create proper JSON response
        self.assertEqual(crawl_link(), proper_response)
        return

    def relevant_to_rpi(self):
        proper_response = ""  # TODO: Create proper JSON response
        self.assertEqual(crawl_link(), proper_response)
        return

    def faulty_link(self):
        proper_response = ""  # TODO: Create proper JSON response
        self.assertEqual(crawl_link(), proper_response)
        return

    def no_robots_violation(self):
        proper_response = ""  # TODO: Create proper JSON response
        self.assertEqual(crawl_link(), proper_response)
        return

class TestSoupPy(unittest.TestCase):
    
    #Crawl a URL that does exist, is revelant to RPI, has a valid robots.txt and sitemap.xml with a last modified date and change frequency
    #This is the base case test for a proper webpage. The modified json should modify the data handscraped from the webpage below
    def crawlSuccess(self):
        
    #Attempt to crawl a URL that doesn't exist. The modified json should have an error code of 404 because the page cannot be found
    def crawlFail(self):
        
    #Crawl a URL that isn't relevant to RPI. The modified json should have an error code of 600 to signify the page isn't relevant
    def crawlNotRelevant(self):
        
    #Attempt to access a robots.txt from a URL that does have a robots.txt. Then, use that robots.txt to return all disallowed links.
    def crawlRobotsTxtExists(self):
    
    #Attempt to access a robots.txt form a URL that doesn't have a robots.txt.
    def crawRobotsTxtDoesntExist(self):

class TestErrors(unittest.TestCase):
    def no_tests_yet(self):
        return


class TestLoad(unittest.TestCase):
    def no_tests_yet(self):
        return


class TestEthics(unittest.TestCase):
    def no_tests_yet(self):
        return

    
if __name__ == "__main__":
    unittest.main()
