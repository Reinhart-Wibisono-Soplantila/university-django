from django.contrib import admin
from .models import TeachingStaff, AdministrativeStaff, PositionTeachingStaff, AreaOfExpertise

# Register your models here.

@admin.register(TeachingStaff)
class TeachingStaffAdmin(admin.ModelAdmin):
    list_display=['nip', 'fullname', 'position', 'faculty', 'department']
    search_fields=['fullname']
    list_filter=['faculty', 'department', 'position']
    ordering=['nip']

@admin.register(AdministrativeStaff)
class AdministrativeStaffAdmin(admin.ModelAdmin):
    list_display=['nip', 'fullname', 'faculty', 'department']
    search_fields=['fullname']
    list_filter=['faculty', 'department']
    ordering=['nip']

@admin.register(PositionTeachingStaff)
class PositionTeachingStaffAdmin(admin.ModelAdmin):
    list_display=['position_name', 'created_at', 'updated_at']
    search_fields=['position_name']
    
@admin.register(AreaOfExpertise)
class AreaOfExpertiseAdmin(admin.ModelAdmin):
    list_display=['expertise_field', 'created_at', 'updated_at']
    search_fields=['expertise_field']