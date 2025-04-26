from django.urls import path
from .views import StudentAPIView, FacultyAutocomplete, DepartmentAutocomplete

app_name='app_student'
urlpatterns = [
    path('', StudentAPIView.as_view(), name='get_all'),
    path('<str:student_nim>', StudentAPIView.as_view(), name='get_specific'),
    # # path('profile/<str:student_nim>', StudentProfileApiView.as_view(), name='get_specific'),
    
    path('faculty-autocomplete/', FacultyAutocomplete.as_view(), name='faculty-autocomplete'),
    path('department-autocomplete/', DepartmentAutocomplete.as_view(), name='department-autocomplete'),
]
