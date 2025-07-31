from rest_framework import serializers

from .models import Resource, Skill, ResourceAvailability

class ResourceAvailabilitySerializer(serializers.ModelSerializer):
    resource_name = serializers.CharField(source='resource.name', read_only=True)
    class Meta:
        model = ResourceAvailability
        fields = "__all__"

class ResourceSerializer(serializers.ModelSerializer):
    manager = serializers.SerializerMethodField()
    skills = serializers.SerializerMethodField()
    availability = serializers.SerializerMethodField()
    
    def get_manager(self, obj):
        return obj.manager.name if obj.manager else None
    
    def get_skills(self, obj):
        return [
            _skill.name
            for _skill in obj.skills.all()
        ]
    
    def get_availability(self, obj):
        return [
            {
                "available_from": _avl.available_from,
                "available_to": _avl.available_to,
                "is_available": _avl.is_available
            }
            for _avl in obj.availabilities.all()
        ]
    
    def validate(self, data):
        allowed_fields = set(self.fields.keys())
        unexpected_fields = set(data.keys()) - allowed_fields
        
        if unexpected_fields:
            raise serializers.ValidationError(
                f"Invalid fields: {', '.join(unexpected_fields)}"
            )
    
    class Meta:
        model = Resource
        fields = "__all__"
        
class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
