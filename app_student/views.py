from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import Student
from .serializers import *
from app_common.models import Faculty, Department
from university.response import *
from dal import autocomplete

# Create your views here.
class StudentAPIView(APIView):
    def get(self, request, student_nim=None):
        if student_nim is not None:
            student_obj=get_object_or_404(Student, nim=student_nim)
            serializer=StudentSerializer_Get(student_obj)
        else:
            student_obj=Student.objects.all()
            serializer=StudentSerializer_Get(student_obj, many=True)
        return success_response(serializer.data, message="success retrive data")
    
    def post(self, request):
        serializer=StudentSerializer_Create(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError("error: ", {error_clean})
    
    # def put(self, request, student_nim):
    #     student_obj=get_object_or_404(Student, nim=student_nim)
    #     serializer=StudentSerializer_Put(student_obj, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         serializer.save()
    #         return success_response(serializer.data, message="success update data")
    #     except IntegrityError as e:
    #         error_clean = str(e).replace('\n', ' ').replace('"', '')
    #         raise ValidationError({error_clean})
    
    def patch(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        serializer=StudentSerializer_Update(student_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        student_obj.user.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)

class FacultyAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Faculty.objects.all()
        print(qs)
        if self.q:
            qs = qs.filter(faculty_name__icontains=self.q)

        return qs
    
class DepartmentAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        faculty_id = self.forwarded.get('faculty', None)  # Dapatkan faculty_id dari form
        qs = Department.objects.all()
        
        if faculty_id:
            qs = qs.filter(faculty_id=faculty_id)  # Filter department berdasarkan faculty
        
        if self.q:
            qs = qs.filter(department_name__icontains=self.q)
        
        return qs