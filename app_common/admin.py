from django.contrib import admin
from .models import Grade, Status, Term, Faculty, Department

# Register your models here.
@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display=['faculty_code', 'faculty_name', 'created_at', 'updated_at']
    search_fields=['faculty_name']
    ordering=['faculty_code', 'created_at', 'updated_at']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display=['department_code', 'department_name', 'faculty', 'created_at', 'updated_at']
    search_fields=['departem_code']
    list_filter=['faculty']
    ordering=['department_code', 'created_at', 'updated_at']

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