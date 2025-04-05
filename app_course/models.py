from django.db import models
from django.utils import timezone
from app_common.models import Department, Faculty

# Create your models here.
class CourseType(models.Model):
    type=models.CharField(max_length=10)
    abbreviation=models.CharField(max_length=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.type
    
class Course(models.Model):
    course_id=models.CharField(max_length=30, db_index=True, editable=False, unique=True)
    course_name=models.CharField(max_length=255)
    foreign_name=models.CharField(max_length=255)
    type=models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='courses')
    sks=models.IntegerField()
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course')
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    is_course_public=models.IntegerField(default=0, choices=[(0, "Non Public"), (1, "Public")])
    is_active=models.IntegerField(default=1, choices=[(0, "Inactive"), (1, "Active")])
    level=models.IntegerField(choices=[(0, "S1"), (1, "S2"), (2, "S3")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.course_id:
            department=self.department.id
            faculty=self.department.faculty.faculty_code
            year=timezone.now().year
            last_course=Course.objects.order_by('-id').first()
            last_number=int(last_course.course_id[-4:])+1 if last_course else 1
            # last_number = course.count() + 1 if course.exists() else 0
            
            self.course_id=f"{faculty}{department:02d}1{year}1{last_number:04d}"
        super().save(*args, **kwargs) # Call the real save() method
    
    def __str__(self):
        return self.course_name
        