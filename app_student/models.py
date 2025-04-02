from django.db import models
from app_common.models import Faculty, Department, Status, Grade
from app_course.models import Course
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.timezone import now

# Create your models here.
class Student(models.Model):
    nim=models.CharField(max_length=15, db_index=True, unique=True, editable=False)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="student_faculty")
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name="student_department")
    registration_year = models.IntegerField(default=now().year)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.nim:
            faculty_code=self.faculty.faculty_code
            department_code=self.department.id
            year=str(self.registration_year)[-2:]
            last_student=Student.objects.filter(registration_year=self.registration_year, department=self.department).order_by('-nim').first()
            if last_student:
                student_number=int(last_student.nim[-3:])+1
            else:
                student_number=1
            self.nim=f'{faculty_code}{department_code:02d}1{year}1{student_number:03d}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nim
    
class StudentProfile(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, editable=False)
    fullname=models.CharField(max_length=255)
    phone_number=PhoneNumberField()
    address=models.TextField()
    city_birth=models.CharField(max_length=255)
    date_birth=models.DateField()
    email=models.EmailField()
    status=models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.student.nim
    
class StudentResult(models.Model):
    registered_schedule = models.ForeignKey("app_schedule.RegisteredSchedule", on_delete=models.CASCADE, related_name="results")
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, related_name="results")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='results')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.registered_schedule}-{self.registered_schedule.student.nim}"
    
        