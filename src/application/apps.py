import os
import subprocess
import sys
from pathlib import Path

from django.apps import AppConfig


class ApplicationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "application"

    def ready(self):
        if os.environ.get("DJANGO_DEBUG", "False").lower() != "true":
            return
        if os.environ.get("SIMULATE_PAYMENTS_ON_START", "0") != "1":
            return
        if os.environ.get("RUN_MAIN") != "true":
            return

        if os.environ.get("SIMULATE_PAYMENTS_RUNNING") == "1":
            return

        os.environ["SIMULATE_PAYMENTS_RUNNING"] = "1"

        interval = os.environ.get("SIMULATE_PAYMENTS_INTERVAL", "2")
        clear_flag = "--clear" if os.environ.get("SIMULATE_PAYMENTS_CLEAR", "1") == "1" else ""
        manage_dir = Path(__file__).resolve().parent.parent
        command = [sys.executable, "manage.py", "simulate_payments", "--interval", interval]
        if clear_flag:
            command.append(clear_flag)

        subprocess.Popen(
            command,
            cwd=str(manage_dir),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
