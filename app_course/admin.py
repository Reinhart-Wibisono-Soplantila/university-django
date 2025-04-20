from django.contrib import admin
from .models import Course, CourseType

# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['id','course_id', 'course_name', 'foreign_name', 'course_type', 'is_specific', 'is_course_public', 'is_active']
    search_fields=['course_name']
    list_filter=['faculty', 'course_type', 'is_course_public', 'is_active']
    ordering=['course_id']
    
@admin.register(CourseType)
class CourseTypeAdmin(admin.ModelAdmin):
    list_display=['type', 'abbreviation', 'created_at', 'updated_at']
    search_fields=['type']
