import uuid

from django.db import models

from api.common.models import TimeStampedModel
from api.v1.manager.models import Manager

class Skill(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
  
    class Meta:
        db_table = 'skill'
   
class Resource(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    skills = models.ManyToManyField(Skill, related_name='resources')
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(Manager, related_name='resources', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'resource'

class ResourceAvailability(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    resource = models.ForeignKey(Resource, related_name='availabilities', on_delete=models.CASCADE)
    available_from = models.DateField()
    available_to = models.DateField()
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.resource.name}: {self.start_date} to {self.end_date}"

    class Meta:
        db_table = 'resource_availability'

