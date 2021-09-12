from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'users'

    def ready(self):
        """avoids unwanted import side effects"""
        import users.signals



