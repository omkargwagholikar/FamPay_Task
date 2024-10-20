import os
import sys

from django.apps import AppConfig
from django.db.models.signals import post_migrate


class FampayTaskConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "FamPay_Task"

    def ready(self):

        if os.environ.get("RUN_MAIN") == "true" and "runserver" in sys.argv:
            from . import scheduler_config

            scheduler_config.initialize()
