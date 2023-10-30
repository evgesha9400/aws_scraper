import unittest

from src.index import handler


class LambdaHandlerTest(unittest.TestCase):
    @classmethod
    def test_scrape(cls):
        handler(None, None)
