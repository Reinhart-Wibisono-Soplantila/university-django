from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .models import Course, CourseType
from .serializers import CourseSerializer, CourseTypeSerializer
from django.core.cache import cache
from django.db import transaction
from university.permissions import isAdminStaff, isAdmin 
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

# Create your views here.
class CourseTypeApiView(APIView):
    CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated, isAdmin]
    
    @staticmethod
    def clear_cache_courseType(coursetype_id=None):
        keys=["courseType_All"]
        if coursetype_id:
            keys.append(f"courseType_{coursetype_id}")
        cache.delete_many(keys)
        
    def get_queryset(self):
        return Course.objects.select_related('course_type', 'faculty', 'academic_program')
        
    def get(self, request, coursetype_id=None):
        cache_key=f"courseType_{coursetype_id}" if coursetype_id else "courseType_All"
        data=cache.get(cache_key)
        if not data:
            if coursetype_id is not None:
                coursetype_obj=get_object_or_404(self.get_queryset(), id=coursetype_id)
                serializer=CourseTypeSerializer(coursetype_obj)
            else:
                coursetype_obj=self.get_queryset().all()
                serializer=CourseTypeSerializer(coursetype_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrive data')
    
    def post(self, request):
        serializer=CourseTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                CourseTypeApiView.clear_cache_courseType()
                return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def put(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(self.get_queryset(), id=coursetype_id)
        serializer=CourseTypeSerializer(coursetype_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                CourseTypeApiView.clear_cache_courseType(coursetype_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(self.get_queryset(), id=coursetype_id)
        serializer=CourseTypeSerializer(coursetype_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                CourseTypeApiView.clear_cache_courseType(coursetype_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(self.get_queryset(), id=coursetype_id)
        try:
            with transaction.atomic():
                coursetype_obj.delete()
                CourseTypeApiView.clear_cache_courseType(coursetype_id)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

class CourseApiView(APIView):
    CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated, isAdminStaff]
    
    @staticmethod
    def clear_cache_course(course_id=None):
        keys=["course_all"]
        if course_id:
            keys.append(f"course_{course_id}")
        cache.delete_many(keys)
        
    def get_queryset(self):
        return Course.objects.select_related("course_type", "faculty", "academic_program")
    
    def get(self, request, course_id=None):
        cache_key=f"course_{course_id}" if course_id else "course_all"
        data=cache.get(cache_key)
        if not data:
            if course_id is not None:
                course_obj=get_object_or_404(self.get_queryset(), course_id=course_id)
                serializer=CourseSerializer(course_obj)
            else:
                course_obj=self.get_queryset().all()
                serializer=CourseSerializer(course_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrive data')
    
    def post(self, request):
        serializer=CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                CourseApiView.clear_cache_course()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, course_id):
        course_obj=get_object_or_404(Course, course_id=course_id)
        serializer=CourseSerializer(course_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                CourseApiView.clear_cache_course(course_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, course_id):
        course_obj=get_object_or_404(Course, course_id=course_id)
        serializer=CourseSerializer(course_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                CourseApiView.clear_cache_course(course_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, course_id):
        course_obj=get_object_or_404(Course, course_id=course_id)
        try:
            with transaction.atomic():
                course_obj.delete()
                CourseApiView.clear_cache_course(course_id)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            