import os
import sys

import django
from django.db import transaction

sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from api.v1.resource.models import Skill


skills = [
    {"name": "Python", "description": "Python programming"},
    {"name": "Django", "description": "Django web framework"},
    {"name": "Django REST Framework", "description": "API development with Django REST Framework"},
    {"name": "React", "description": "Frontend development with React"},
    {"name": "TypeScript", "description": "Typed JavaScript for frontend development"},
    {"name": "SQL", "description": "Database querying and management"},
    {"name": "PostgreSQL", "description": "Relational database system"},
    {"name": "Kafka", "description": "Real-time stream processing"},
    {"name": "PyTorch", "description": "Deep learning framework"},
    {"name": "TensorFlow", "description": "Machine learning library by Google"},
    {"name": "Pandas", "description": "Data manipulation and analysis"},
    {"name": "Scikit-learn", "description": "Machine learning algorithms and tools"},
    {"name": "Cryptography", "description": "Data encryption and security"},
    {"name": "OAuth2", "description": "Authentication protocol"},
    {"name": "Docker", "description": "Containerization platform"},
    {"name": "Git", "description": "Version control system"},
]

with transaction.atomic():
    for _skill in skills:
        Skill.objects.get_or_create(
            name=_skill['name'],
            defaults={"description": _skill['description']}
        )
