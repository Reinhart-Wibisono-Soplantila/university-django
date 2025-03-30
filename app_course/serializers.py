from rest_framework import serializers
from .models import Course, CourseType

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'
        read_only_fields=['course_id']

class CourseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseType
        fields='__all__'