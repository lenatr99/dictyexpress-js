# dictyexpress_backend/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dictyexpress_backend.settings')

app = Celery('dictyexpress_backend')

# Load settings from Django settings with "CELERY_" namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all installed apps
app.autodiscover_tasks()
