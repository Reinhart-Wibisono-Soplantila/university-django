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
            coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
            serializer=CourseTypeSerializer(coursetype_obj, many=True)
        return success_response(serializer.data, message='success retrive data')
    
    def post(self, request):
        serializer=CourseTypeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
        
    def put(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
        serializer=CourseTypeSerializer(coursetype_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
        
    def put(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
        serializer=CourseTypeSerializer(coursetype_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def delete(self, request, coursetype_id):
        coursetype_obj=get_object_or_404(CourseType, id=coursetype_id)
        coursetype_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
            