from django.db import models

# Create your models here.
class Building(models.Model):
    building_name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)

class Room(models.Model):
    building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name="rooms")
    room_name=models.CharField(max_length=255)
    capacity=models.IntegerField

class Faculty(models.Model):
    faculty_code=models.CharField(max_length=5, db_index=True, unique=True)
    building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name="faculties")
    faculty_name=models.CharField(max_length=255)

class Department(models.Model):
    department_code=models.CharField(max_length=4, db_index=True, unique=True, editable=False)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")
    department_name=models.CharField(max_length=255)