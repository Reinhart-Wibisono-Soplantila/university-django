from django.contrib import admin
from .models import *
from .forms import StudentForm

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display=['nim', 'faculty', 'department', 'registration_year']
    search_fields=['nim']
    list_filter=['faculty']
    ordering=['nim']
    autocomplete_fields = ['faculty']
    
# admin.site.register(StudentResult)
