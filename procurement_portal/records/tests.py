from unittest.mock import MagicMock, patch
import html5lib
from django.contrib.messages import ERROR
from django.contrib.admin.sites import AdminSite
from django.test import Client, TestCase

from .signals import build_error_message
from .models import DatasetVersion
from .admin import DatasetVersionAdmin, admin


class AdminTestCase(TestCase):
    def setUp(self):
        self.my_model_admin = DatasetVersionAdmin(model=DatasetVersion, admin_site=AdminSite())
        self.instance = DatasetVersion()

    def test_error_message_file_upload(self):
        request_mock = MagicMock()
        with patch.object(admin.ModelAdmin, 'save_model'):
            with patch("procurement_portal.records.admin.messages") as messages_mock:
                self.instance._error_message = "Message"
                self.my_model_admin.save_model(obj=self.instance, request=request_mock, form=None, change=None)

                messages_mock.set_level.assert_called_once_with(request_mock, messages_mock.ERROR)
                messages_mock.add_message.assert_called_once_with(request_mock, messages_mock.ERROR, "Message")

    def test_lack_of_error_message_file_upload(self):
        request_mock = MagicMock()
        with patch.object(admin.ModelAdmin, 'save_model'):
            with patch("procurement_portal.records.admin.messages") as messages_mock:
                self.my_model_admin.save_model(obj=self.instance, request=request_mock, form=None, change=None)

                messages_mock.set_level.assert_not_called()
                messages_mock.add_message.assert_not_called()


class BuildErrorMessageTestCase(TestCase):
    def setUp(self):
        error = MagicMock(__str__=MagicMock(return_value="[<Exception>]"))
        row = {"Column": "Value"}
        row_error = (1, (MagicMock(error=error, row=row),))
        self.result_mock = MagicMock(
            row_errors=MagicMock(return_value=[row_error])
        )

    def test_build_error_message(self):
        expected_message = "Parsing error(s)<br/>Invalid rows:<br/>Row: 1<br/>errors: ['Exception']<br/>values: Value"
        self.assertEqual(build_error_message(self.result_mock), expected_message)


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
