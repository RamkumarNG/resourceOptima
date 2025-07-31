import uuid

from django.db import models

from api.v1.manager.models import Manager
from api.v1.resource.models import Resource, ResourceAvailability
from api.v1.resource.models import Skill
from api.common.models import TimeStampedModel

class Project(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True, related_name='projects')
    assigned_resource_status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('partial assigned', 'Partial Assigned'), ('not assigned', 'Not Assigned')])

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'project'

class Task(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    skill_required = models.ManyToManyField(Skill, related_name='tasks')
    start_date = models.DateField()
    end_date = models.DateField() 
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.project.name})"

    class Meta:
        db_table = 'task'
        
class TaskAssignment(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name="assignment")
    resource = models.OneToOneField(Resource, on_delete=models.CASCADE, related_name='assignee')
    availability = models.OneToOneField(ResourceAvailability, on_delete=models.CASCADE, related_name='task_assignment')
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task"],
                name="unique_task_assignment",
            )
        ]
