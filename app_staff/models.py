from django.db import models
from app_common.models import Faculty, Department
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User

# Create your models here.
class PositionTeachingStaff(models.Model):
    position_name=models.CharField(max_length=30, unique=True, db_index=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.position_name

class AreaOfExpertise(models.Model):
    expertise_field=models.CharField(max_length=100, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.expertise_field

class SuperAdminStaff(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='super_admin')
    nip=models.CharField(max_length=30, db_index=True,unique=True)
    full_name=models.CharField(max_length=255)
    phone_number=PhoneNumberField(unique=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nip}-{self.fullname}"
    

class TeachingStaff(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='teaching_staff')
    nip=models.CharField(max_length=30, db_index=True,unique=True)
    full_name=models.CharField(max_length=255)
    position=models.ForeignKey(PositionTeachingStaff, on_delete=models.CASCADE, related_name="teaching_staff")
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="teaching_staff")
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name="teaching_staff")
    areas_of_expertise=models.ManyToManyField(AreaOfExpertise, related_name="teaching_staff")
    phone_number=PhoneNumberField(unique=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nip}-{self.fullname}"
    
class AdministrativeStaff(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name='administrative_staff')
    nip=models.CharField(max_length=30, db_index=True,unique=True)
    full_name=models.CharField(max_length=255)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="administrative_staff")
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name="administrative_staff")
    phone_number=PhoneNumberField(unique=True)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nip}-{self.fullname}"