from django.urls import path
from .views import CourseApiView, CourseTypeApiView

app_name='app_course'
urlpatterns = [
    path('', CourseApiView.as_view(), name='all_course'),
    path('<str:course_id>', CourseApiView.as_view(), name='specific_course'),
    path('type/', CourseTypeApiView.as_view(), name='all_course_type'),
    path('type/<int:coursetype_id>', CourseTypeApiView.as_view(), name='specific_course_type')
]