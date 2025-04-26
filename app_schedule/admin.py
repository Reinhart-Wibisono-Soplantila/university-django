# from django.contrib import admin
# from .models import RegisteredSchedule, Schedule

# # Register your models here.
# @admin.register(Schedule)
# class ScheduleAdmin(admin.ModelAdmin):
#     list_display=['id','get_course_name', 'building', 'room', 'day_held', 'time_start', 'time_finish', 'max_quota', 'registered_quota', 'remaining_quota']
    
#     def get_course_name(self, obj):
#         return obj.course.course_name
#     get_course_name.short_description='Course Name'
# admin.site.register(RegisteredSchedule)