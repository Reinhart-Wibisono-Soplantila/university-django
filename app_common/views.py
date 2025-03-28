from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Grade, Term, Status, Faculty, Department
from .serializers import GradeSerializer, TermSerializers, StatusSerializers, FacultySerializer, DepartmentSerializer
from university.response import *

# Create your views here.
class GradeApiView(APIView):
    def get(self, request, grade_id=None):
        if grade_id is not None:
            grade_obj=get_object_or_404(Grade, id=grade_id)
            serializer=GradeSerializer(grade_obj)
        else:
            grade_obj=Grade.objects.all()
            serializer=GradeSerializer(grade_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
        
    def post(self, request):
        serializer=GradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return created_response(serializer.data, message='success create data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})

    def put(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def patch(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def delete(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        grade_obj.delete()
        return delete_reponse()
        # return Response({
        #     "status_code":status.HTTP_200_OK,
        #     "status":"success",
        #     "message":"success delete data",
        # }, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class TermApiView(APIView):
    def get(self, request, term_code=None):
        if term_code is not None:
            term_obj=get_object_or_404(Term, term_code=term_code)
            serializer=TermSerializers(term_obj)
        else:
            term_obj=Term.objects.all()
            serializer=TermSerializers(term_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=TermSerializers(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def put(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        serializer=TermSerializers(term_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def patch(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        serializer=TermSerializers(term_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def delete(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        term_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class StatusApiView(APIView):
    def get(self, request, status_id=None):
        if status_id is not None:
            status_obj=get_object_or_404(Status, id=status_id)
            serializer=StatusSerializers(status_obj)
        else:
            status_obj=Status.objects.all()
            serializer=StatusSerializers(status_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=StatusSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            serializer.save()
            return created_response(serializer.data, message="success created data")
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def put(self, request, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        serializer=StatusSerializers(status_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def patch(self, request, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        serializer=StatusSerializers(status_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
    
    def delete(self, requqest, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        status_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
 
class FacultyApiView(APIView):
    def get(self, request, faculty_id=None):
        if faculty_id is not None:
            faculty_obj=get_object_or_404(Faculty, id=faculty_id)
            serializer=FacultySerializer(faculty_obj)
        else:
            faculty_obj=Faculty.objects.all()
            serializer=FacultySerializer(faculty_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=FacultySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            serializer.save()
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})

    def put(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
        
    def patch(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})

    def delete(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        faculty_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class DepartmentApiView(APIView):
    def get(self, request, department_id=None):
        if department_id is not None:
            department_obj=get_object_or_404(Department, id=department_id)
            serializer=DepartmentSerializer(department_obj)
        else:
            department_obj=Department.objects.all()
            serializer=DepartmentSerializer(department_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})

    def put(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})
        
    def patch(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise ValidationError({"detail": "Integrity error: " + str(e)})

    def delete(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        department_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    