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
    academic_program_id=serializers.PrimaryKeyRelatedField(
        queryset=AcademicProgram.objects.all(),
        write_only=True,
        required=True,
        source='academic_program',
        error_messages={
            'does_not_exist': 'Academic Program dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Academic Program ID harus berupa angka',
            'required': 'Field Academic Program harus diisi!'})
    
    faculty=FacultySerializer(read_only=True)
    faculty_id=serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        write_only=True,
        required=True,
        source='faculty',
        error_messages={
            'does_not_exist': 'Faculty dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Faculty ID harus berupa angka',
            'required': 'Field Faculty harus diisi!'})
    
    course_type=CourseTypeSerializer(read_only=True)
    course_type_id=serializers.PrimaryKeyRelatedField(
        queryset=CourseType.objects.all(),
        write_only=True,
        required=True,
        source='course_type',
        error_messages={
            'does_not_exist': 'Course Type dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Course Type ID harus berupa angka',
            'required': 'Field Course Type harus diisi!'})
    
    class Meta:
        model=Course
        fields='__all__'
        read_only_fields=['course_id']
    
    def update(self, instance, validated_data):
        academic_program_changed = 'academic_program' in validated_data and validated_data['academic_program'] != instance.academic_program
        faculty_changed = 'faculty' in validated_data and validated_data['faculty'] != instance.faculty

        if academic_program_changed or faculty_changed:
            faculty=validated_data.get('faculty', instance.faculty)
            academic_program=validated_data.get('academic_program', instance.academic_program)
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
        for field in ["faculty", "academic_program", "course_type"]:
            if field in rep and rep[field] is not None:
                rep[field].pop("created_at", None)
                rep[field].pop("updated_at", None)
        return rep