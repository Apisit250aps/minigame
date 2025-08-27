from django.core.management import call_command
import os
import django
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "minigame.settings")
django.setup()


filename = f"data.json"

with open(filename, "w", encoding="utf-8") as f:
    call_command("dumpdata", indent=2, stdout=f)

print(f"Data dumped to {filename}")
