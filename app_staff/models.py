from django.db import models
from app_common.models import Faculty, Department
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class PositionTeachingStaff(models.Model):
    position_name=models.CharField(max_length=30, unique=True, db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
class TeachingStaff(models.Model):
    nip=models.IntegerField(db_index=True, unique=True)
    fullname=models.CharField(max_length=255)
    position=models.ForeignKey(PositionTeachingStaff, on_delete=models.CASCADE, related_name="teaching_staffs")
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="teaching_staffs")
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teaching_staffs")
    areas_of_expertise=models.TextField()
    email=models.EmailField()
    phone_number=PhoneNumberField(unique=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class AdministrativeStaff(models.Model):
    nip=models.IntegerField(db_index=True, unique=True)
    fullname=models.CharField(max_length=255)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="administrative_staff")
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name="administrative_staff")
    email=models.EmailField()
    phone_number=PhoneNumberField(unique=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)