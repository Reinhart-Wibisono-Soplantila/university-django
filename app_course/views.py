from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .models import Course, CourseType
from .serializers import CourseSerializer, CourseTypeSerializer

# Create your views here.
class CourseTypeApiView(APIView):
    def get(self, request, coursetype_id=None):
        if coursetype_id is not None:
            coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
            serializer=CourseTypeSerializer(coursetype_obj)
        else:
            coursetype_obj=CourseType.objects.all()
            serializer=CourseTypeSerializer(coursetype_obj, many=True)
        return success_response(serializer.data, message='success retrive data')
    
    def post(self, request):
        serializer=CourseTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def put(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
        serializer=CourseTypeSerializer(coursetype_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
        serializer=CourseTypeSerializer(coursetype_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
        coursetype_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)

class CourseApiView(APIView):
    def get(self, request, course_id=None):
        if course_id is not None:
            course_obj=get_object_or_404(Course, course_id=course_id)
            serializer=CourseSerializer(course_obj)
        else:
            course_obj=Course.objects.all()
            serializer=CourseSerializer(course_obj, many=True)
        return success_response(serializer.data, message='success retrive data')
    
    def post(self, request):
        serializer=CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, course_id):
        course_obj=get_object_or_404(Course, course_id=course_id)
        serializer=CourseSerializer(course_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, course_id):
        course_obj=get_object_or_404(Course, course_id=course_id)
        serializer=CourseSerializer(course_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, course_id):
        course_obj=get_object_or_404(Course, course_id=course_id)
        course_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
            