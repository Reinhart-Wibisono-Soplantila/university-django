from django.contrib import admin
from .models import Student, StudentProfile, StudentResult
from .forms import StudentForm

# Register your models here.
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    form = StudentForm
    list_display=['nim', 'faculty', 'department', 'registration_year']
    search_fields=['nim']
    list_filter=['faculty']
    ordering=['nim']
    # autocomplete_fields = ['faculty']

@admin.register(StudentProfile)
class STudentProfileAdmin(admin.ModelAdmin):
    list_display=['get_nim', 'fullname', 'email', 'status']
    search_fields=['nim']
    list_filter=['status']
    
    def get_nim(self, obj):
        return obj.student.nim
    get_nim.admin_order_field='student__nim'
    get_nim.short_description = 'NIM'
    
admin.site.register(StudentResult)
