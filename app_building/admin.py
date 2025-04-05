from django.contrib import admin
from .models import Building, Room

# Register your models here.
@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display=['building_name', 'faculty', 'address', 'is_public']
    search_fields=['building_name']
    list_filter=['faculty']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display=['building', 'room_name', 'capacity']
    search_fields=['room_name']
    list_filter=['building']