from django.contrib import admin
from .models import Grade, Status, Term, Faculty, Department

# Register your models here.
class FacultyAdmin(admin.ModelAdmin):
    search_fields=['faculty_id']

admin.site.register(Grade)
admin.site.register(Status)
admin.site.register(Term)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Department)