from django.apps import AppConfig
import logging

class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

    def ready(self):
        # Log every time the app is ready
        logging.info("Store app is ready and models are being registered.")
