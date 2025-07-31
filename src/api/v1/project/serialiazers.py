from rest_framework import serializers

from .models import Project, Task, Skill, TaskAssignment
from api.v1.manager.models import Manager

class TaskAssignemtSerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    
    class Meta:
        model = TaskAssignment
        fields = ['resource_name']


class TaskSerializer(serializers.ModelSerializer):
    skills = serializers.SerializerMethodField()
    assignment = serializers.SerializerMethodField()
    
    def get_skills(self, obj):
        return list(obj.skill_required.values_list('name', flat=True))
    
    def get_assignment(self, obj):
        if self.context.get('deep_fetch'):
            assignment = getattr(obj, 'assignment', None)
            if assignment:
                return TaskAssignemtSerializer(assignment).data
            
        return None
    
    class Meta:
        model = Task
        fields = ['name', 'start_date', 'end_date', 'is_active', 'skills', 'assignment']


#For PATCH requests, DRF automatically ignores the required=True constraint for fields that are not included in the payload — because PATCH is a partial update.
class ProjectSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    manager = serializers.SerializerMethodField()
    manager_email = serializers.EmailField(write_only=True, required=False)
    
    def get_manager(self, obj):
        return obj.manager.name if obj.manager else None
    
    def update(self, instace, validated_data):
        manager_email = validated_data.pop('manager_email', None)
        if manager_email:
            manager = Manager.objects.get(email=manager_email)
            instace.manager=manager
            
        
        for attr, value in validated_data.items():
            setattr(instace, attr, value)
        
        instace.save()
        return instace
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'manager', 'manager_email', 'tasks']

