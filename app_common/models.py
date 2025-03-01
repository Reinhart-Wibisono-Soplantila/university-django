from django.db import models

# Create your models here.
class Term(models.Model):
    semester_choices=[
        (1, "Semester 1"),
        (2, "Semester 2")
    ]
    term_code=models.CharField(max_length=10, unique=True, db_index=True)
    year_start=models.IntegerField()
    year_end=models.IntegerField()
    semester=models.IntegerField(choices=semester_choices)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.year_start}/{self.year_end}-Semester {self.semester}"
    
class Grade(models.Model):
    numerical_grade=models.DecimalField(max_digits=3, decimal_places=2)
    alphabet_grade=models.CharField(max_length=2, unique=True) 
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.alphabet_grade

class Status(models.Model):
    status_name=models.CharField(max_length=100, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.status_name