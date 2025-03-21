from .views import CourseApiView, CourseTypeApiView
from django.urls import path

app_name='app_course'
urlpatterns = [
    path('', CourseApiView.as_view, name='get all course'),
    path('<str:course_id>', CourseApiView.as_view, name='get specific course'),
    path('type/', CourseTypeApiView.as_view, name='get all course type'),
    path('type/<int:coursetype_id>', CourseTypeApiView.as_view, name='get specific course type'),
]