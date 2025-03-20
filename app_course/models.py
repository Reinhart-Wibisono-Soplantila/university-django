from django.db import models
from app_staff.models import TeachingStaff
from app_common.models import Department

# Create your models here.
class CourseType(models.Model):
    type=models.CharField(max_length=10)
    abbreviation=models.CharField(max_length=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class Course(models.Model):
    course_id=models.CharField(max_length=30, db_index=True, editable=False, unique=True)
    course_name=models.CharField(max_length=255)
    foreign_name=models.CharField(max_length=255)
    type=models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='courses')
    sks=models.IntegerField()
    teaching_staff=models.ForeignKey(TeachingStaff, on_delete=models.CASCADE, related_name='courses')
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    is_course_public=models.IntegerField()
    is_active=models.IntegerField()
    educational_level=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)