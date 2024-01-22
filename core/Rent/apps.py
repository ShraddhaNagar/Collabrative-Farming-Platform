from django.apps import AppConfig


class RentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Rent'

    # def ready(self):
    #     import Rent.signals
