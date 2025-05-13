from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializer import ScheduleSerializer
from .models import Schedule
from university.response import *
from django.core.cache import cache
from django.db import transaction

# Create your views here.
class ScheduleApiView(APIView):
    CACHE_TIMEOUT=60*60
    
    def get_queryset(self):
        return Schedule.objects.select_related(
            "course", 
            "building", 
            "room", 
            "teaching_staff", 
            "department"
            )
    
    @staticmethod
    def clear_cache_schedule(schedule_id=None):
        keys=["schedule_all"]
        if schedule_id:
            keys.append(f"schedule_{schedule_id}")
        cache.delete_many(keys)
    
    def get(self, request, schedule_id=None):
        cache_key=f"schedule_{schedule_id}" if schedule_id else "schedule_all"
        data=cache.get(cache_key)
        if not data:
            if schedule_id is not None:
                schedule_obj=get_object_or_404(self.get_queryset(), id=schedule_id)
                serializer=ScheduleSerializer(schedule_obj)
            else:
                schedule_obj=self.get_queryset().all()
                serializer=ScheduleSerializer(schedule_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=ScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                ScheduleApiView.clear_cache_schedule()
                return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            return Response(
                {"detail": "Integrity error: " + str(e)},
                status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, schedule_id):
        schedule_obj=get_object_or_404(self.get_queryset(), id=schedule_id)
        serializer=ScheduleSerializer(schedule_obj)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                ScheduleApiView.clear_cache_schedule(schedule_id)
                return success_response(serializer.data, message='success udpate data')
        except IntegrityError as e:
            return ValidationError({"detail": "Integrity error: " + str(e)})
        
    def patch(self, request, schedule_id):
        schedule_obj=get_object_or_404(self.get_queryset(), id=schedule_id)
        serializer=ScheduleSerializer(schedule_obj, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                ScheduleApiView.clear_cache_schedule(schedule_id)
                return success_response(serializer.data, message='success udpate data')
        except IntegrityError as e:
            return ValidationError({"detail": "Integrity error: " + str(e)})
        
    def delete(self, request, schedule_id):
        schedule_obj=get_object_or_404(self.get_queryset(), id=schedule_id)
        try:
            with transaction.atomic():
                schedule_obj.delete()
                ScheduleApiView.clear_cache_schedule(schedule_id)
                return delete_response()
        except IntegrityError as e:
            return ValidationError({"detail": "Integrity error: " + str(e)})