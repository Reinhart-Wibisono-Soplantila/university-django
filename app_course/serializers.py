from rest_framework import serializers
from .models import *
from django.utils import timezone
from app_common.serializers import AcademicProgramSerializer, FacultySerializer
from django.shortcuts import get_object_or_404

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
    
    def validate_academic_program_id(self, value):
        if not AcademicProgram.objects.filter(id=value).exists():
            raise serializers.ValidationError("Academic Program dengan ID ini tidak valid")
        return value
    
    def validate_faculty_id(self, value):
        if not Faculty.objects.filter(id=value).exists():
            raise serializers.ValidationError("Faculty dengan ID ini tidak valid")
        return value
    
    def validate_course_type_id(self, value):
        if not CourseType.objects.filter(id=value).exists():
            raise serializers.ValidationError("Course Type dengan ID ini tidak valid")
        return value
    
    def create(self, validated_data):
        faculty_id=validated_data.pop('faculty_id')
        academic_program_id=validated_data.pop('academic_program_id')
        course_type_id=validated_data.pop('course_type_id')
        
        faculty=get_object_or_404(Faculty, id=faculty_id)
        academic_program=get_object_or_404(AcademicProgram, id=academic_program_id)
        course_type=get_object_or_404(CourseType, id=course_type_id)
        
        validated_data['faculty']=faculty
        validated_data['academic_program']=academic_program
        validated_data['course_type']=course_type
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        academic_program=instance.academic_program
        if 'academic_program_id' in validated_data:
            academic_program_id = validated_data.pop('academic_program_id', None)
            if academic_program_id is not None and academic_program_id != instance.academic_program.id:
                academic_program = get_object_or_404(AcademicProgram, id=academic_program_id)
                validated_data['academic_program'] = academic_program
        
        faculty=instance.faculty
        if 'faculty_id' in validated_data:
            faculty_id=validated_data.pop('faculty_id', None)
            if faculty_id is not None and faculty_id != instance.faculty.id:
                faculty = get_object_or_404(Faculty, id=faculty_id)
                validated_data['faculty'] = faculty
                
        course_type_id=validated_data.get('course_type_id', None)
        if course_type_id:
            validated_data['course_type'] = get_object_or_404(CourseType, id=course_type_id)
        
        generate_new_code =  (
            'academic_program_id' in validated_data or
            'faculty_id' in validated_data or
            'is_specific' in validated_data)
        
        if generate_new_code:
            is_specific=validated_data.get('is_specific', instance.is_specific)
            if is_specific==1:
                last_course=Course.objects.filter(faculty_id=faculty.id, is_specific=1, academic_program_id=academic_program.id).exclude(id=instance.id).order_by('-id').first()
                academic_program=academic_program.academic_program_code
                academic_number=int(academic_program[-3:])
                faculty=faculty.faculty_code
                year=str(timezone.now().year)[-2:]
                
                last_number=int(last_course.course_id[-3:])+1 if last_course else 1
                validated_data['course_id']=f"{faculty}{academic_number:03d}1{year}1{last_number:03d}"
            elif is_specific==0:
                last_course=Course.objects.filter(faculty_id=faculty.id,is_specific=0).exclude(id=instance.id).order_by('-id').first()
                
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