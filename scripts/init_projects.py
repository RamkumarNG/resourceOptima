import os
import sys
import django

sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from api.v1.project.models import Project
from api.v1.manager.models import Manager
from django.db import transaction

projects = [
    {
        "name": "VitalTrack",
        "description": (
            "A real-time patient monitoring system that uses IoT devices to collect vitals like heart rate, "
            "blood pressure, and oxygen levels, with AI-driven anomaly detection for early warnings."
        ),
    },
    {
        "name": "MediAlert AI",
        "description": (
            "An AI-powered alert system for ICUs that predicts critical events such as cardiac arrest or sepsis "
            "using continuous patient data streams."
        ),
    },
    {
        "name": "HealthVault",
        "description": (
            "A real-time medication tracking system that ensures the right medication is delivered to the right patient "
            "at the right time using barcode scanning and AI-based schedule optimization."
        ),
        "manager": "zidane@example.com",
    },
]


with transaction.atomic():
    for _project in projects:
        Project.objects.get_or_create(
            name=_project['name'],
            description=_project['description'],
            manager = Manager.objects.get(email=_project.get("manager")) if _project.get("manager") else None
        )
