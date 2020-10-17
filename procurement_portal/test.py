import html5lib
from django.test import Client, TestCase


class IndexTestCase(TestCase):
    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertContains(
            response,
            "homepage for procurement_portal",
        )
        assertValidHTML(response.content)


def assertValidHTML(string):
    """
    Raises exception if the string is not valid HTML, e.g. has unmatched tags
    that need to be matched.
    """
    parser = html5lib.HTMLParser(strict=True)
    parser.parse(string)
