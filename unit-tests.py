
import unittest
from crawler_server import crawl_link


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
