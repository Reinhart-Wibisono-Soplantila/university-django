from rest_framework import serializers
from .models import Course, CourseType

class CourseSerializer(serializers):
    class Meta:
        model='Course'
        fields="__all__"

class CourseTypeSerializer(serializers):
    class Meta:
        model='CourseType'
        fields='__all__'