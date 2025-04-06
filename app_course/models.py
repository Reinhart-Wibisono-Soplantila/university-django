from django.db import models
from django.utils import timezone
from app_common.models import Department, Faculty, AcademicProgram

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
    course_type=models.ForeignKey(CourseType, on_delete=models.CASCADE, related_name='courses')
    sks=models.IntegerField()
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='course')
    academic_program=models.ForeignKey(AcademicProgram, on_delete=models.CASCADE, related_name='course')
    # department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    is_course_public=models.IntegerField(default=0, choices=[(0, "Non Public"), (1, "Public")])
    is_active=models.IntegerField(default=1, choices=[(0, "Inactive"), (1, "Active")])
    is_specific=models.IntegerField(choices=[(0, "Non Specific"), (1, "Specific")])
    # level=models.IntegerField(choices=[(0, "S1"), (1, "S2"), (2, "S3")])
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.course_id:
            if self.is_specific==1:
                academic_program=self.academic_program
                faculty=self.faculty
                last_course=Course.objects.filter(faculty_id=faculty, is_specific=1, academic_program_id=academic_program).order_by('-course_id').first()
                
                faculty=faculty.faculty_code
                academic_number=int(academic_program.academic_program_code[-3:])
                year=str(timezone.now().year)[-2:]
                
                last_number=int(last_course.course_id[-3:])+1 if last_course else 1
                self.course_id=f"{faculty}{academic_number:03d}1{year}1{last_number:03d}"
            else:
                faculty=self.faculty
                last_course=Course.objects.filter(faculty_id=faculty, is_specific=0).order_by('-course_id').first()
                
                faculty=faculty.faculty_code
                year=str(timezone.now().year)[-2:]
                
                last_number=int(last_course.course_id[-3:])+1 if last_course else 1
                self.course_id=f"{faculty}1{year}1{last_number:03d}"
        super().save(*args, **kwargs) # Call the real save() method
    
    def __str__(self):
        return self.course_name
        