from django.apps import AppConfig
from django.test import Client
from django.urls import reverse


class RecordsConfig(AppConfig):
    name = "procurement_portal.records"

    def ready(self):
        import procurement_portal.records.signals  # noqa

        save_xlsx_template()


def save_xlsx_template():
    print("Saving template.xlsx")
    client = Client()
    res = client.get(reverse("purchase-records-template-xlsx"))
    with open("template.xlsx", "wb") as file:
        file.write(res.content)
    print("Saved template.xlsx")
