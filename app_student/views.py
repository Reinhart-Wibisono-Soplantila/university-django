from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import Student
from .serializers import StudentSerializer
from university.response import *

# Create your views here.
class StudentAPIView(APIView):
    def get(self, request, student_nim=None):
        if student_nim is not None:
            student_obj=get_object_or_404(Student, nim=student_nim)
            serializer=StudentSerializer(student_obj)
        else:
            student_obj=Student.objects.all()
            serializer=StudentSerializer(student_obj, many=True)
        return success_response(serializer, message="success retrive data")
    
    def post(self, request):
        serializer=StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(serializer, message="success create data")
        # return error_400_response(serializer)
    
    def put(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        serializer=StudentSerializer(student_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(serializer, message="success update data")
        # return error_400_response(serializer)
    
    def patch(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        serializer=StudentSerializer(student_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success_response(serializer, message="success update data")
        # return error_400_response(serializer)
    
    def delete(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        student_obj.delete()
        return delete_reponse(message="success delete data")
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)