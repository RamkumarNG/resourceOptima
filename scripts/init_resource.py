import os
import sys
from datetime import date

import django
from django.db import transaction

sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from api.v1.resource.models import Resource, Skill, ResourceAvailability
from api.v1.manager.models import Manager



resources = [
    {
        "name": "Pedri González",
        "email": "pedri@example.com",
        "skills": ["Python", "Django", "Django REST Framework", "SQL"],
        "manager": "xavi@example.com",
        "availability": [
            {"available_from": date(2024, 7, 10), "available_to": date(2024, 7, 25)},
            {"available_from": date(2024, 7, 30), "available_to": date(2024, 8, 5)}
        ]
    },
    {
        "name": "Jude Bellingham",
        "email": "jude@example.com",
        "skills": ["React", "TypeScript", "Git"],
        "manager": "eden@example.com",
        "availability": [
            {"available_from": date(2024, 7, 15), "available_to": date(2024, 7, 25)}
        ]
    },
    {
        "name": "Ter Stegen",
        "email": "stegen@example.com",
        "skills": ["Python", "SQL", "Kafka"],
        "manager": "xavi@example.com",
        "availability": [
            {"available_from": date(2024, 7, 20), "available_to": date(2024, 8, 5)}
        ]
    },
    {
        "name": "Ansu Fati",
        "email": "ansu@example.com",
        "skills": ["PyTorch", "Scikit-learn", "Pandas"],
        "manager": "eden@example.com",
        "availability": [
            {"available_from": date(2024, 7, 18), "available_to": date(2024, 7, 31)}
        ]
    },
    {
        "name": "Frenkie de Jong",
        "email": "frenkie@example.com",
        "skills": ["Python", "Cryptography", "PostgreSQL"],
        "manager": "xavi@example.com",
        "availability": [
            {"available_from": date(2024, 7, 16), "available_to": date(2024, 7, 28)}
        ]
    },
    {
        "name": "Gavi Paez",
        "email": "gavi@example.com",
        "skills": ["Django", "OAuth2", "Docker"],
        "manager": "eden@example.com",
        "availability": [
            {"available_from": date(2024, 7, 22), "available_to": date(2024, 8, 2)}
        ]
    },
]

with transaction.atomic():
    for _res in resources:
        manager_obj = Manager.objects.get(email=_res['manager'])

        resource, _ = Resource.objects.get_or_create(
            email=_res['email'],
            defaults={"name": _res['name'], "is_active": True, "manager": manager_obj}
        )

        for skill_name in _res['skills']:
            skill = Skill.objects.get(name=skill_name)
            resource.skills.add(skill)

        for avail in _res['availability']:
            ResourceAvailability.objects.update_or_create(
                resource=resource,
                available_from=avail['available_from'],
                available_to=avail['available_to'],
                defaults={"is_available": True}
            )
