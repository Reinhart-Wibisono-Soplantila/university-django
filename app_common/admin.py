from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display=['numerical_grade', 'alphabet_grade', 'created_at', 'updated_at']
    ordering=['numerical_grade', 'alphabet_grade', 'created_at', 'updated_at']
    
@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display=['status_name', 'created_at', 'updated_at']
    ordering=['created_at', 'updated_at']

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display=['term_code', 'year_start', 'year_end', 'semester', 'is_active']
    search_fields=['term_code', 'year_start', 'year_end']
    list_filter=['semester', 'is_active']
    
@admin.register(EducationLevel)
class EducationLevelAdmin(admin.ModelAdmin):
    list_display=['education_name', 'abbreviation', 'foreign_name']
    search_fields=['education_name', 'foreign_name']
    list_filter=['education_name', 'foreign_name']
        
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display=['faculty_code', 'faculty_name', 'created_at', 'updated_at']
    search_fields=['faculty_name']
    ordering=['faculty_code', 'created_at', 'updated_at']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=['department_code', 'department_name', 'faculty']
    search_fields=['department_name']
    list_filter=['faculty']
    ordering=['department_code', 'created_at', 'updated_at']

@admin.register(AcademicProgram)
class AcademicProgramAdmin(admin.ModelAdmin):
    list_display=['id', 'academic_program_code', 'academic_program_name', 'faculty', 'education_level']
    search_fields=['academic_program_code', 'academic_program_name']
    list_filter=['faculty', 'education_level']
    ordering=['academic_program_code']