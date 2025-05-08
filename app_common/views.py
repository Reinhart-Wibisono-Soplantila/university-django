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

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class TermApiView(APIView):
    CACHE_TIMEOUT = 60*60
    def get(self, request, term_code=None):
        if term_code is not None:
            cache_key=f"term_{term_code}"
            cache_data=cache.get(cache_key)
            if not cache_data:
                term_obj=get_object_or_404(Term, term_code=term_code)
                serializer=TermSerializers(term_obj)
                data=serializer.data
                cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        else:
            cache_key="term_all"
            cache_data=cache.get(cache_key)
            if not cache_data:
                term_obj=Term.objects.all()
                serializer=TermSerializers(term_obj, many=True)
                data=serializer.data
                cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=TermSerializers(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            cache.delete("term_all")
            return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        serializer=TermSerializers(term_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            cache.delete(f"term_{term_code}")
            cache.delete("term_all")
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        serializer=TermSerializers(term_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            cache.delete(f"term_{term_code}")
            cache.delete("term_all")
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def delete(self, request, term_code):
        term_obj=get_object_or_404(Term, term_code=term_code)
        try:
            term_obj.delete()
            cache.delete(f"term_{term_code}")
            cache.delete("term_all")
            return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
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
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        serializer=StatusSerializers(status_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, status_id):
        status_obj=get_object_or_404(Status, id=status_id)
        serializer=StatusSerializers(status_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
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
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def put(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

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
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def put(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def delete(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        department_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class EducationLevelApiView(APIView):
    def get(self, request, edulevel_id=None):
        if edulevel_id is not None:
            edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
            serializer=EducationLevelSerializer(edulevel_obj)
        else:
            edulevel_obj=EducationLevel.objects.all()
            serializer=EducationLevelSerializer(edulevel_obj, many=True)
        return success_response(serializer.data, message="success retrieve all data")
    
    def post(self, request):
        serializer=EducationLevelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, edulevel_id):
        edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
        serializer=EducationLevelSerializer(edulevel_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, edulevel_id):
        edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
        serializer=EducationLevelSerializer(edulevel_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def delete(self, request, edulevel_id):
        edulevel_obj=get_object_or_404(EducationLevel, id=edulevel_id)
        edulevel_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class AcademicProgramApiView(APIView):
    def get(self, request, program_id=None):
        if program_id is not None:
            program_obj=get_object_or_404(AcademicProgram, id=program_id)
            serializer=AcademicProgramSerializer(program_obj)
        else:
            program_obj=AcademicProgram.objects.all()
            serializer=AcademicProgramSerializer(program_obj, many=True)
        return success_response(serializer.data, message="success retrieve all data")
    
    def post(self, request):
        serializer=AcademicProgramSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def put(self, request, program_id):
        program_obj=get_object_or_404(AcademicProgram, id=program_id)
        serializer=AcademicProgramSerializer(program_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def patch(self, request, program_id):
        program_obj=get_object_or_404(AcademicProgram, id=program_id)
        serializer=AcademicProgramSerializer(program_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def delete(self, request, program_id):
        program_obj=get_object_or_404(AcademicProgram, id=program_id)
        program_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)