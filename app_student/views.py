from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Student
from .serializers import *
from app_common.models import Faculty, Department
from university.response import *
from dal import autocomplete
from django.core.cache import cache
from django.db import transaction

# Create your views here.
class StudentAPIView(APIView):
    CACHE_TIMEOUT=60*60
    
    def get_queryset(self):
        return Student.objects.select_related('faculty', 'department', 'status').prefetch_related('user', 'user__groups')
    
    @staticmethod
    def clear_cache_student(student_nim=None):
        keys=['student_all']
        if student_nim:
            keys.append(f"student_{student_nim}")
        cache.delete_many(keys)
    
    def get(self, request, student_nim=None):
        cache_key=f"student_{student_nim}" if student_nim else "student_all"
        data=cache.get(cache_key)
        if not data:
            if student_nim is not None:
                student_obj=get_object_or_404(self.get_queryset(), nim=student_nim)
                serializer=StudentSerializer_Get(student_obj)
            else:
                student_obj=self.get_queryset().all()
                serializer=StudentSerializer_Get(student_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message="success retrive data")
    
    def post(self, request):
        serializer=StudentSerializer_Create(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                StudentAPIView.clear_cache_student()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, student_nim):
        student_obj=get_object_or_404(self.get_queryset(), nim=student_nim)
        serializer=StudentSerializer_Update(student_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                StudentAPIView.clear_cache_student(student_nim)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, student_nim):
        student_obj=get_object_or_404(self.get_queryset(), nim=student_nim)
        try:
            with transaction.atomic():
                student_obj.user.delete()
                StudentAPIView.clear_cache_student()
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

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