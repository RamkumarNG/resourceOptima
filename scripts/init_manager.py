import os
import sys
import django

sys.path.append('/app/src')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

django.setup()

from api.v1.manager.models import Manager
from django.db import transaction

managers = [
    {"name": "Manager Xavi", "email": "xavi@example.com"},
    {"name": "Manager Eden", "email": "eden@example.com"},
    {"name": "Manager Zidane", "email": "zidane@example.com"},
]

with transaction.atomic():
    for _mgr in managers:
        Manager.objects.get_or_create(
            email=_mgr['email'],
            defaults={"name": _mgr['name'], "is_active": True}
        )
