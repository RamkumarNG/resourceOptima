import logging

from django.db import transaction
from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from api.v1.manager.models import Manager
from api.v1.manager.serialiazers import ManagerSerializer
from api.common.decorators import handle_exceptions

logger = logging.getLogger(__name__)

class ManagerViewSet(ModelViewSet):
    queryset = Manager.objects.filter(
        Q(is_active=True) | Q(is_active__isnull=True)
    ).prefetch_related(
        'resources', 'projects'
    )
    
    serializer_class = ManagerSerializer

    @handle_exceptions  
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Managers retreieved successfully",
                "data": serializer.data
            }
        })
    
    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        manager_obj = self.get_object()
        serializer = self.get_serializer(manager_obj)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Manager retrieved successfully",
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
                "message": "Manager Created sucessfully",
                "data": serializer_data.data,
            }
        })
    
    @handle_exceptions
    def destroy(self, request, *args, **kwargs):
        manager_obj = self.get_object()
        manager_obj.delete()
        return Response({
            "status": status.HTTP_204_NO_CONTENT,
            "data": {
                "message": "Manager deleted Successfully",
            }
        })
    