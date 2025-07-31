import os
import sys
from datetime import date

import django
from django.db import transaction

sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()


from api.v1.project.models import Project, Task
from api.v1.resource.models import Skill


tasks = [
    {
        "project_name": "VitalTrack",
        "name": "Patient Data API Development",
        "skills": ["Python", "Django REST Framework"],
        "start_date": date(2024, 7, 12),
        "end_date": date(2024, 7, 18),
    },
    {
        "project_name": "VitalTrack",
        "name": "Build Admin Dashboard",
        "skills": ["React", "TypeScript"],
        "start_date": date(2024, 7, 20),
        "end_date": date(2024, 7, 26),
    },
    {
        "project_name": "MediAlert AI",
        "name": "Integrate Real-Time Monitoring",
        "skills": ["Kafka", "Python"],
        "start_date": date(2024, 7, 22),
        "end_date": date(2024, 7, 30),
    },
    {
        "project_name": "MediAlert AI",
        "name": "Train Alert Classification Model",
        "skills": ["PyTorch", "Pandas", "Scikit-learn"],
        "start_date": date(2024, 7, 19),
        "end_date": date(2024, 7, 28),
    },
    {
        "project_name": "HealthVault",
        "name": "Implement Data Encryption Layer",
        "skills": ["Python", "Cryptography"],
        "start_date": date(2024, 7, 17),
        "end_date": date(2024, 7, 22),
    },
    {
        "project_name": "HealthVault",
        "name": "Develop OAuth2 Authentication",
        "skills": ["Django", "OAuth2"],
        "start_date": date(2024, 7, 25),
        "end_date": date(2024, 7, 30),
    },
]

with transaction.atomic():
    for _task in tasks:
        project = Project.objects.get(name=_task['project_name'])
        task_obj, created = Task.objects.get_or_create(
            project=project,
            name=_task['name'],
            start_date=_task['start_date'],
            end_date=_task['end_date'],
            defaults={"is_active": True}
        )

        for _skill in _task['skills']:
            _skill_obj = Skill.objects.get(name=_skill)
            task_obj.skill_required.add(_skill_obj)
