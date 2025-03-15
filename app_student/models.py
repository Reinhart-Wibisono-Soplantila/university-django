from django.db import models

# Create your models here.
class Student(models.Model):
    nim=models.CharField(max_length=15, db_index=True, unique=True)
    fullname=models.CharField(max_length=255)
    