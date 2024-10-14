import sys
import os
import django.core.management

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "coffee.settings.production")

# Intentemos ejecutar el servidor sin autoreload
django.core.management.execute_from_command_line(["manage.py", "runserver", "0.0.0.0:8000", "--noreload"])