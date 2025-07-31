import uuid

from django.db import models

from api.common.models import TimeStampedModel

class Manager(TimeStampedModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(blank=True, null=True, default=True)
    
    def __str__(self):
        return f"{self.name} <{self.email}>"
    
    class Meta:
        db_table = 'manager'
        