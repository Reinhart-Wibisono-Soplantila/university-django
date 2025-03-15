from django.db import models
from app_common.models import Faculty, Department, Status
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Student(models.Model):
    nim=models.CharField(max_length=15, db_index=True, unique=True)
    fullname=models.CharField(max_length=255)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="student_faculty")
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name="student_department")
    phone_number=PhoneNumberField()
    address=models.TextField()
    city_birth=models.CharField(max_length=255)
    date_birth=models.DateField()
    email=models.EmailField()
    status=models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    