from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from .models import Student, StudentProfile
from .serializers import StudentSerializer, StudentProfileSerializer
from app_common.models import Faculty, Department
from university.response import *
from dal import autocomplete

# Create your views here.
class StudentAPIView(APIView):
    def get(self, request, student_nim=None):
        if student_nim is not None:
            student_obj=get_object_or_404(Student, nim=student_nim)
            student_profile_obj=get_object_or_404(StudentProfile, student=student_obj)
            student_data = StudentSerializer(student_obj).data
            student_profile_data = StudentProfileSerializer(student_profile_obj).data if student_profile_obj else None
            data = {**student_data, "profile": student_profile_data}
        else:
            student_obj=Student.objects.all()
            data=StudentSerializer(student_obj, many=True).data
        return success_response(data, message="success retrive data")
    
    def post(self, request):
        serializer=StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    # def put(self, request, student_nim):
    #     student_obj=get_object_or_404(Student, nim=student_nim)
    #     serializer=StudentSerializer(student_obj, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         serializer.save()
    #         return success_response(serializer.data, message="success update data")
    #     except IntegrityError as e:
    #         raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    # def patch(self, request, student_nim):
    #     student_obj=get_object_or_404(Student, nim=student_nim)
    #     serializer=StudentSerializer(student_obj, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         serializer.save()
    #         return success_response(serializer.data, message="success update data")
    #     except IntegrityError as e:
    #         raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def delete(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        student_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class StudentProfileApiView(APIView):
    def get(self, request, student_nim):
        student_obj=get_object_or_404(Student, nim=student_nim)
        studentprofile_obj=get_object_or_404(StudentProfile, student=student_obj)
        stduent_serializer=StudentSerializer(student_obj).data
        studentprofile_serializer=StudentProfileSerializer(studentprofile_obj).data if studentprofile_obj else None
        data={**stduent_serializer, "profile": studentprofile_serializer}
        return success_response(data, message="success retrive data")
    
#     def post(self, request):
#         serializer=StudentSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         try:
#             serializer.save()
#             return success_response(serializer.data, message="success create data")
#         except IntegrityError as e:
#             raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    # def put(self, request, student_nim):
    #     student_obj=get_object_or_404(Student, nim=student_nim)
    #     studentprofile_obj=get_object_or_404(StudentProfile, student=student_obj)
    #     serializer=StudentProfileSerializer(studentprofile_obj, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         serializer.save()
    #         return success_response(serializer.data, message="success update data")
    #     except IntegrityError as e:
    #         raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def patch(self, request, student_nim):
        studentprofile_obj=get_object_or_404(StudentProfile.objects.select_related('student'), student__nim=student_nim)
        serializer=StudentProfileSerializer(studentprofile_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
#     def delete(self, request, student_nim):
#         student_obj=get_object_or_404(Student, nim=student_nim)
#         student_obj.delete()
#         return delete_reponse()
    
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