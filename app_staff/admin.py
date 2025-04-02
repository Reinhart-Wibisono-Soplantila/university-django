from django.contrib import admin
from .models import TeachingStaff, AdministrativeStaff, PositionTeachingStaff, AreaOfExpertise

# Register your models here.
admin.site.register(TeachingStaff)
admin.site.register(AdministrativeStaff)
admin.site.register(PositionTeachingStaff)
admin.site.register(AreaOfExpertise)