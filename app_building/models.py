from django.db import models
from app_common.models import Faculty

# Create your models here.
class Building(models.Model):
    building_name=models.CharField(max_length=255)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name="buildings", blank=True, null=True)
    address=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Room(models.Model):
    building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name="rooms")
    room_name=models.CharField(max_length=255)
    capacity=models.IntegerField(default=25)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)