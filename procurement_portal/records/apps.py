from django.apps import AppConfig


class RecordsConfig(AppConfig):
    name = "procurement_portal.records"

    def ready(self):
        import procurement_portal.records.signals  # noqa
