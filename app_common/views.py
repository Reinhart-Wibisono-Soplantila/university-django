from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from .models import *
from .serializers import *
from university.response import *
from django.core.cache import cache
from django.db import transaction

# Create your views here.
class GradeApiView(APIView):
    CACHE_TIMEOUT = 60*60
    
    @staticmethod
    def clear_grade_cache(grade_id=None):
        keys=["grade_all"]
        if grade_id:
            keys.append(f"grade_{grade_id}")
        cache.delete_many(keys)
        
    def get(self, request, grade_id=None):
        cache_key = f"grade_{grade_id}" if grade_id else "grade_all"
        data=cache.get(cache_key)
        if not data:
            if grade_id is not None:
                grade_obj=get_object_or_404(Grade, id=grade_id)
                serializer=GradeSerializer(grade_obj)
            else:
                grade_obj=Grade.objects.all()
                serializer=GradeSerializer(grade_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
        
    def post(self, request):
        serializer=GradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_grade_cache()
                return created_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def put(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_grade_cache(grade_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
    
    def patch(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_grade_cache(grade_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
    
    def delete(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        try:
            with transaction.atomic():
                grade_obj.delete()
                self.clear_grade_cache(grade_id)
                return delete_reponse(grade_id)
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
    
class TermApiView(APIView):
    CACHE_TIMEOUT = 60*60
    
    @staticmethod
    def clear_cache_term(term_code=None):
        keys=["term_all"]
        if term_code:
            keys.append(f"term_{term_code}")
        cache.delete_many(keys)
        
    def get(self, request, term_code=None):
        cache_key=f"term_{term_code}"
        data=cache.get(cache_key)
        if not data:
            if term_code is not None:
                term_obj=get_object_or_404(Term, term_code=term_code)
                serializer=TermSerializers(term_obj)
            else:
                term_obj=Term.objects.all()
                serializer=TermSerializers(term_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=TermSerializers(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_term()
                return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def put(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        serializer=TermSerializers(term_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_term(term_code)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def patch(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        serializer=TermSerializers(term_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_term(term_code)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def delete(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        try:
            with transaction.atomic():
                term_obj.delete()
                self.clear_cache_term(term_code)
                return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
    
class StatusApiView(APIView):
    CACHE_TIMEOUT=60*60
    
    @staticmethod
    def clear_cache_status(status_id=None):
        keys=['status_all']
        if status_id:
            keys.append(f"status_{status_id}")
        cache.delete_many(keys)
    
    def get(self, request, status_id=None):
        cache_key=f"status_{status_id}" if status_id else "status_all"
        data=cache.get(cache_key)
        if not data:
            if status_id is not None:
                status_obj=get_object_or_404(Status, id=status_id)
                serializer=StatusSerializers(status_obj)
            else:
                status_obj=Status.objects.all()
                serializer=StatusSerializers(status_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=StatusSerializers(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            with transaction.atomic():
                serializer.save()
                self.clear_cache_status()
                return created_response(serializer.data, message="success created data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def put(self, request, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        serializer=StatusSerializers(status_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic:
                serializer.save()
                self.clear_cache_status(status_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def patch(self, request, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        serializer=StatusSerializers(status_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_status(status_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def delete(self, requqest, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        try:
            with transaction.atomic():
                status_obj.delete()
                self.clear_cache_status(status_id)
                return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
 
class FacultyApiView(APIView):
    CACHE_TIMEOUT=60*60
    
    @staticmethod
    def clear_cache_faculty(faculty_id=None):
        keys=["faculty_all"]
        if faculty_id:
            keys.append(f"faculty_{faculty_id}")
        cache.delete_many(keys)
    
    def get(self, request, faculty_id=None):
        cache_key=f"faculty_{faculty_id}" if faculty_id else "faculty_all"
        data=cache.get(cache_key)
        if not data:    
            if faculty_id is not None:
                faculty_obj=get_object_or_404(Faculty, id=faculty_id)
                serializer=FacultySerializer(faculty_obj)
            else:
                faculty_obj=Faculty.objects.all()
                serializer=FacultySerializer(faculty_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=FacultySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try: 
            with transaction.atomic():
                serializer.save()
                self.clear_cache_faculty()
                return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})

    def put(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_faculty(faculty_id)    
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
        
    def patch(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_faculty(faculty_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})

    def delete(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        try:
            with transaction.atomic():
                
                faculty_obj.delete()
                self.clear_cache_faculty(faculty_id)
                return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
                
class DepartmentApiView(APIView):
    CACHE_TIMEOUT=60*60
    
    @staticmethod
    def clear_cache_department(department_id=None):
        keys=['department_all']
        if department_id:
            keys.append(f"department_{department_id}")
        cache.delete_many(keys)
        
    def get_queryset(self):
        return Department.objects.select_related("faculty")
    
    
    def get(self, request, department_id=None):
        cache_key=f"department_{department_id}" if department_id else "department_all"
        data=cache.get(cache_key)
        if not data:
            if department_id is not None:
                department_obj=get_object_or_404(self.get_queryset(), id=department_id)
                serializer=DepartmentSerializer(department_obj)
            else:
                department_obj=self.get_queryset().all()
                serializer=DepartmentSerializer(department_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_department()
                return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def put(self, request, department_id):
        department_obj=get_object_or_404(self.get_queryset(), id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_department(department_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def patch(self, request, department_id):
        department_obj=get_object_or_404(self.get_queryset(), id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_department(department_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def delete(self, request, department_id):
        department_obj=get_object_or_404(self.get_queryset(), id=department_id)
        try:
            with transaction.atomic():
                department_obj.delete()
                self.clear_cache_department(department_id)
                return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})

class EducationLevelApiView(APIView):
    CACHE_TIMEOUT = 60*60
    
    @staticmethod
    def clear_cache_edulevel(edulevel_id=None):
        keys=["edulevel_all"]
        if edulevel_id:
            keys.append(f"edulevel_{edulevel_id}")
        cache.delete_many(keys)
    
    def get(self, request, edulevel_id=None):
        cache_key=f"edulevel_{edulevel_id}" if edulevel_id else "edulevel_all"
        data=cache.get(cache_key)
        if not data:
            if edulevel_id is not None:
                edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
                serializer=EducationLevelSerializer(edulevel_obj)
            else:
                edulevel_obj=EducationLevel.objects.all()
                serializer=EducationLevelSerializer(edulevel_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message="success retrieve all data")
    
    def post(self, request):
        serializer=EducationLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_edulevel()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, edulevel_id):
        edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
        serializer=EducationLevelSerializer(edulevel_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_edulevel(edulevel_id)    
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, edulevel_id):
        edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
        serializer=EducationLevelSerializer(edulevel_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_edulevel(edulevel_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def delete(self, request, edulevel_id):
        edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
        try:
            with transaction.atomic():
                edulevel_obj.delete()
                self.clear_cache_edulevel(edulevel_id)
                return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
class AcademicProgramApiView(APIView):
    CACHE_TIMEOUT=60*60
    
    def get_queryset(self):
        return AcademicProgram.objects.select_related("faculty", "education_level")
    
    @staticmethod
    def clear_cache_academicProgram(program_id=None):
        keys=["program_all"]
        if program_id:
            keys.append(f"program_{program_id}")
        cache.delete_many(keys)
    
    def get(self, request, program_id=None):
        cache_key=f"program_{program_id}" if program_id else "program_all"
        data=cache.get(cache_key)
        if not data:
            if program_id is not None:
                program_obj=get_object_or_404(self.get_queryset(), id=program_id)
                serializer=AcademicProgramSerializer(program_obj)
            else:
                program_obj=self.get_queryset().all()
                serializer=AcademicProgramSerializer(program_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(serializer.data, message="success retrieve all data")
    
    def post(self, request):
        serializer=AcademicProgramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_academicProgram()
                return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, program_id):
        program_obj=get_object_or_404(self.get_queryset(), id=program_id)
        serializer=AcademicProgramSerializer(program_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_academicProgram(program_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, program_id):
        program_obj=get_object_or_404(self.get_queryset(), id=program_id)
        serializer=AcademicProgramSerializer(program_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                self.clear_cache_academicProgram(program_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def delete(self, request, program_id):
        program_obj=get_object_or_404(self.get_queryset(), id=program_id)
        try:
            with transaction.atomic():
                program_obj.delete()
                self.clear_cache_academicProgram(program_id)
                return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)