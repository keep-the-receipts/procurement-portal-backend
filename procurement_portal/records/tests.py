from unittest.mock import MagicMock, patch
import html5lib
from django.contrib.messages import ERROR
from django.contrib.admin.sites import AdminSite
from django.test import Client, TestCase


class IndexTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get("/records")
        self.assertContains(
            response,
            "index for records in procurement_portal",
        )
        assertValidHTML(response.content)


def assertValidHTML(string):
    """
    Raises exception if the string is not valid HTML, e.g. has unmatched tags
    that need to be matched.
    """
    parser = html5lib.HTMLParser(strict=True)
    parser.parse(string)
