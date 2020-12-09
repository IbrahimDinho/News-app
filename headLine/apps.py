from django.apps import AppConfig


class HeadlineConfig(AppConfig):
    name = 'headLine'

    def ready(self):
        print("App Ready")

