from django.contrib import admin
from .models import RegisteredSchedule, Schedule

# Register your models here.
admin.site.register(Schedule)
admin.site.register(RegisteredSchedule)