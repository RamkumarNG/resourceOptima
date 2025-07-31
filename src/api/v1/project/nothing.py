import logging

from django.db import transaction
from django.db.models import Q, Count
from django.contrib.postgres.aggregates import ArrayAgg

from api.v1.project.models import *
from api.v1.manager.models import *
from api.v1.resource.models import *

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

tasks_obj = project_obj.tasks.all().annotate(task_skills=ArrayAgg('skill_required__id', distinct=True)).values('start_date', 'end_date', 'task_skills', 'name')

assigned_resource_ids = set(TaskAssignment.objects.values_list('availability__id', flat=True))
logger.info(f'assigned_resource_ids--->{assigned_resource_ids}')
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
    
    logger.info(f'resources_with_skills--->{resources_with_skills}')
    
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
        "message": "Assigned tasks successfully",
        "data": fin
    }
})
    
    # if selected_resource and availability:
    #     with transaction.atomic():
    #         TaskAssignment.objects.create(
    #             task__id=_task.id,
    #             resource__id = selected_resource.id,
    #             availability__id = availability.id
    #         )
        
    #         availability.is_available = False
    #         availability.save()
    

