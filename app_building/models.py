from django.db import models

# Create your models here.
class Building(models.Model):
    budilding_name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)

class Room(models.Model):
    building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name="rooms")
    room_name=models.CharField(max_length=255)
    capacity=models.IntegerField

class Faculty(models.Model):
    faculty_name=models.CharField(max_length=255)

class Department(models.Model):
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="departments")
    department_name=models.CharField(max_length=255)