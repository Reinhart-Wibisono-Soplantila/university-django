from rest_framework import serializers
from .models import Course, CourseType
from django.utils import timezone
from rest_framework.exceptions import ValidationError

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'
        read_only_fields=['course_id']
    
    def update(self, instance, validated_data):
        academic_program=validated_data.get('academic_program', instance.academic_program)
        faculty=validated_data.get('faculty', instance.faculty)
        is_specific=validated_data.get('is_specific', instance.is_specific)
        if academic_program!= instance.academic_program or faculty!=instance.faculty:
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

class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseType
        fields='__all__'