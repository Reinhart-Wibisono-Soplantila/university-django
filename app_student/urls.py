from django.urls import path
from .views import StudentAPIView, StudentProfileApiView

app_name='app_student'
urlpatterns = [
    path('', StudentAPIView.as_view(), name='get_all'),
    path('<str:student_nim>', StudentAPIView.as_view(), name='get_specific'),
    
    
    path('profile/<str:student_nim>', StudentProfileApiView.as_view(), name='get_specific'),
]
