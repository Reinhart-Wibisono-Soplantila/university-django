from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .serializer import ScheduleSerializer
from .models import Schedule
from university.response import *

# Create your views here.
class ScheduleApiView(APIView):
    def get(self, request, schedule_id=None):
        if schedule_id is not None:
            schedule_obj=get_object_or_404(Schedule, id=schedule_id)
            serializer=ScheduleSerializer(schedule_obj)
        else:
            schedule_obj=Schedule.objects.all()
            serializer=ScheduleSerializer(schedule_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=ScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            return ValidationError({"detail": "Integrity error: " + str(e)})
        
    def put(self, request, schedule_id):
        schedule_obj=get_object_or_404(Schedule, id=schedule_id)
        serializer=ScheduleSerializer(schedule_obj)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success udpate data')
        except IntegrityError as e:
            return ValidationError({"detail": "Integrity error: " + str(e)})
        
    def patch(self, request, schedule_id):
        schedule_obj=get_object_or_404(Schedule, id=schedule_id)
        serializer=ScheduleSerializer(schedule_obj, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success udpate data')
        except IntegrityError as e:
            return ValidationError({"detail": "Integrity error: " + str(e)})
        
    def delete(self, request, schedule_id):
        schedule_obj=get_object_or_404(Schedule, id=schedule_id)
        schedule_obj.delete()
        return delete_reponse
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)