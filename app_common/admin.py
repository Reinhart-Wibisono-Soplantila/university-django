from django.contrib import admin
from .models import Grade, Status, Term, Faculty, Department

# Register your models here.
admin.site.register(Grade)
admin.site.register(Status)
admin.site.register(Term)
admin.site.register(Faculty)
admin.site.register(Department)