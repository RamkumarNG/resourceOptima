import logging

from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .models import Resource, Skill, ResourceAvailability
from .serialiazers import ResourceSerializer, SkillSerializer, ResourceAvailabilitySerializer
from api.common.decorators import handle_exceptions

logger = logging.getLogger(__name__)

class ResourceViewSet(ModelViewSet):
    queryset = Resource.objects.filter(Q(is_active=True) | Q(is_active__isnull=True))
    serializer_class = ResourceSerializer
    
    @handle_exceptions  
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Resources retreieved successfully",
                "data": serializer.data
            }
        })
    
    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        Resource_obj = self.get_object()
        serializer = self.get_serializer(Resource_obj)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Resource retrieved successfully",
                "data": serializer.data
            }
        })
        
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        serializer_data = self.get_serializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer_data.save()
        
        return Response({
            "status": status.HTTP_201_CREATED,
            "data": {
                "message": "Resource Created sucessfully",
                "data": serializer_data.data,
            }
        })
    
    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        Resource_obj = self.get_object()
        Resource_obj.delete()
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "data": {
                "message": "Resource deleted Successfully",
            }
        })

class SkillViewSet(ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    
    @handle_exceptions  
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Skills retreieved successfully",
                "data": serializer.data
            }
        })
    
    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        Resource_obj = self.get_object()
        serializer = self.get_serializer(Resource_obj)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Resource retrieved successfully",
                "data": serializer.data
            }
        })
        
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        serializer_data = self.get_serializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer_data.save()
        
        return Response({
            "status": status.HTTP_201_CREATED,
            "data": {
                "message": "Resource Created sucessfully",
                "data": serializer_data.data,
            }
        })
    
    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        Resource_obj = self.get_object()
        Resource_obj.delete()
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "data": {
                "message": "Resource deleted Successfully",
            }
        })
        
class ResourceAvailabilityViewSet(ModelViewSet):
    serializer_class = ResourceAvailabilitySerializer

    def get_queryset(self):
        # Retrieve 'pk' from URL kwargs (the viewset URL conf should pass this)
        resource_id = self.kwargs['resource_pk']
        return ResourceAvailability.objects.select_related('resource').filter(resource__id=resource_id)
    
    @handle_exceptions  
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Resources retreieved successfully",
                "data": serializer.data
            }
        })
    
    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        Resource_obj = self.get_object()
        serializer = self.get_serializer(Resource_obj)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "ResourceAvailability retrieved successfully",
                "data": serializer.data
            }
        })
        
    @handle_exceptions
    def create(self, request, *args, **kwargs):
        serializer_data = self.get_serializer(data=request.data)
        serializer_data.is_valid(raise_exception=True)
        with transaction.atomic():
            serializer_data.save()
        
        return Response({
            "status": status.HTTP_201_CREATED,
            "data": {
                "message": "ResourceAvailability Created sucessfully",
                "data": serializer_data.data,
            }
        })
    
    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        Resource_obj = self.get_object()
        Resource_obj.delete()
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "data": {
                "message": "ResourceAvailability deleted Successfully",
            }
        })
