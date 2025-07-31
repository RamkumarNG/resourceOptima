import logging

from django.db import transaction
from django.db.models import Q, Count
from django.contrib.postgres.aggregates import ArrayAgg

from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Project, TaskAssignment
from api.v1.resource.models import Resource
from api.v1.manager.models import Manager

from .serialiazers import ProjectSerializer
from api.common.decorators import handle_exceptions

logger = logging.getLogger(__name__)

class ProjectViewSet(ModelViewSet):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        deep_fetch = self.request.query_params.get('deep_fetch') == 'true'
        qs = Project.objects.select_related('manager').prefetch_related('tasks', 'tasks__skill_required')

        if deep_fetch:
            qs = qs.prefetch_related('tasks__assignment', 'tasks__assignment__resource')

        return qs
    
    @handle_exceptions  
    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Projects retreieved successfully",
                "data": serializer.data
            }
        })
    
    @handle_exceptions
    def retrieve(self, request, *args, **kwargs):
        deep_fetch = request.query_params.get('deep_fetch') or False
        
        resource_obj = self.get_object()
        serializer = self.get_serializer(resource_obj, context={'deep_fetch': deep_fetch})
        
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Project retrieved successfully",
                "data": serializer.data
            }
        })
        
    
    @handle_exceptions
    def partial_update(self, request, *args, **kwargs):
        project_obj = self.get_object()
        
        serializer = self.get_serializer(project_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Project Updated successfully",
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
                "message": "Project Created sucessfully",
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
                "message": "Project deleted Successfully",
            }
        })

    @action(detail=True, methods=["POST", 'post'], url_path='assign_tasks')
    @handle_exceptions
    def assign_tasks(self, request, *args, **kwargs):
        project_id = kwargs.get('pk')
        assigned = False
        
        project_obj = Project.objects.select_related(
            'manager',
        ).prefetch_related(
            'tasks__skill_required'
        ).get(id=project_id)
        
        if not project_obj.manager:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {"message": "Cannot assign tasks. Project does not have a manager assigned"}
            })
        
        if not project_obj.tasks:
            return Response({
                "status": status.HTTP_400_BAD_REQUEST,
                "data": {"message": "No tasks has been found"}
            })
        
        tasks_obj = project_obj.tasks.all().annotate(
            task_skills=ArrayAgg('skill_required__id', distinct=True)
        ).values('start_date', 'end_date', 'task_skills', 'name', 'id')
        
        assigned_resource_ids = set(TaskAssignment.objects.values_list('availability__id', flat=True))
        fin = {}
        for _task in tasks_obj:
            task_skills = _task['task_skills']
            task_skill_count = len(task_skills)
            
            # Step 1: Get all resources with the required skills and valid availability window
            resources_with_skills = Resource.objects.annotate(
                matched_skills=Count(
                    'skills',
                    filter=Q(skills__in=task_skills),
                    distinct=True 
                )
            ).filter(
                matched_skills=task_skill_count,
                availabilities__available_from__lte=_task['start_date'],
                availabilities__available_to__gte=_task['end_date'],
                availabilities__is_available=True,
            ).exclude(
                 availabilities__id__in=assigned_resource_ids
            ).distinct().prefetch_related(
                'availabilities'
            )
                        
            selected_resource = None
            availability = None
            
            for resource in resources_with_skills:
                for avl in resource.availabilities.all():
                    if (
                        avl.available_from <= _task['start_date'] and
                        avl.available_to >= _task['end_date'] and
                        avl.is_available and
                        avl.id not in assigned_resource_ids
                    ):
                        selected_resource = resource
                        availability = avl
                        break
                
                if selected_resource:
                    break
            
            if selected_resource and availability:
                with transaction.atomic():
                    TaskAssignment.objects.create(
                        task_id = _task['id'],
                        resource = selected_resource,
                        availability = availability
                    )
                
                    availability.is_available = False
                    availability.save()
                    assigned = True
            
            fin[_task['name']] = {
                'skills': task_skills,
                "selected_res": {
                    "id": selected_resource.id,
                    "name": selected_resource.name,
                    "email": selected_resource.email,
                    # add more fields if needed
                } if selected_resource else None,
                "availability": {
                    "id": availability.id,
                    "available_from": availability.available_from,
                    "available_to": availability.available_to,
                    "is_available": availability.is_available
                } if availability else None
            }

        return Response({
            "status": status.HTTP_200_OK,
            "data": {
                "message": "Assigned tasks successfully" if assigned else "No tasks could be allocated due to unavailable resources",
                "data": fin
            }
        })

