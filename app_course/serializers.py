from rest_framework import serializers
from .models import *
from django.utils import timezone
from app_common.serializers import AcademicProgramSerializer, FacultySerializer

class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseType
        fields='__all__'

class CourseSerializer(serializers.ModelSerializer):
    academic_program=AcademicProgramSerializer(read_only=True)
    academic_program_id=serializers.IntegerField(
        write_only=True,
        required=True,
        allow_null=False
    )
    
    faculty=FacultySerializer(read_only=True)
    faculty_id=serializers.IntegerField(
        write_only=True,
        required=True,
        allow_null=False
    )
    
    course_type=CourseTypeSerializer(read_only=True)
    course_type_id=serializers.IntegerField(
        write_only=True,
        required=True,
        allow_null=False
    )
    
    class Meta:
        model=Course
        fields='__all__'
        read_only_fields=['course_id']
    
    def update(self, instance, validated_data):
        academic_program=instance.academic_program
        if 'academic_program_id' in validated_data:
            academic_program_id = validated_data.pop('academic_program_id')
            if academic_program_id != instance.academic_program_id:
                academic_program = AcademicProgram.objects.get(id=academic_program_id)
                validated_data['academic_program'] = academic_program
        
        faculty=instance.faculty
        if 'faculty_id' in validated_data:
            faculty_id=validated_data.pop('faculty_id')
            if faculty_id != instance.faculty_id:
                faculty = Faculty.objects.get(id=faculty_id)
                validated_data['faculty'] = faculty
                
        course_type_id=validated_data.get('course_type_id')
        if course_type_id:
            validated_data['course_type'] = CourseType.objects.get(id=course_type_id)
        
        generate_new_code =  (
            'academic_program_id' in validated_data or
            'faculty_id' in validated_data or
            'is_specific' in validated_data)
        
        if generate_new_code:
            is_specific=validated_data.get('is_specific', instance.is_specific)
            
            if is_specific==1:
                last_course=Course.objects.filter(faculty_id=faculty, is_specific=1, academic_program_id=academic_program).exclude(id=instance.id).order_by('-id').first()
                academic_program=academic_program.academic_program_code
                academic_number=int(academic_program[-3:])
                faculty=faculty.faculty_code
                year=str(timezone.now().year)[-2:]
                
                last_number=int(last_course.course_id[-3:])+1 if last_course else 1
                validated_data['course_id']=f"{faculty}{academic_number:03d}1{year}1{last_number:03d}"
            elif is_specific==0:
                last_course=Course.objects.filter(faculty_id=faculty,is_specific=0).exclude(id=instance.id).order_by('-id').first()
                
                faculty=faculty.faculty_code
                year=str(timezone.now().year)[-2:]
                
                last_number=int(last_course.course_id[-3:])+1 if last_course else 1
                validated_data['course_id']=f"{faculty}1{year}1{last_number:03d}"
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if "faculty" in rep and rep['faculty'] is not None:
            data=rep["faculty"]
            data.pop("created_at", None)
            data.pop("updated_at", None)
        if "academic_program" in rep and rep["academic_program"] is not None:
            data=rep["academic_program"]
            data.pop("created_at", None)
            data.pop("updated_at", None)
        if "course_type" in rep and rep["course_type"] is not None:
            data=rep["course_type"]
            data.pop("created_at", None)
            data.pop("updated_at", None)
        return rep