from rest_framework import serializers

from .models import Manager

#For PATCH requests, DRF automatically ignores the required=True constraint for fields that are not included in the payload — because PATCH is a partial update.
class ManagerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    is_active = serializers.BooleanField(required=True)
    resources = serializers.SerializerMethodField()
    projects = serializers.SerializerMethodField()
    
    def get_resources(self, obj):
        return list(obj.resources.values_list('name', flat=True))
    
    def get_projects(self, obj):
        return list(obj.projects.values_list('projects', flat=True))
    
    class Meta:
        model = Manager
        fields = "__all__"
