from django.contrib import admin
from .models import Student, StudentProfile, StudentResult

# Register your models here.
admin.site.register(Student)
admin.site.register(StudentProfile)
admin.site.register(StudentResult)