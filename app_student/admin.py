from django.contrib import admin
from .models import Student, StudentProfile, StudentResult
from .forms import StudentForm

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display=['nim', 'faculty', 'department', 'registration_year']
    # autocomplete_fields = ['faculty']
    
admin.site.register(StudentProfile)
admin.site.register(StudentResult)
