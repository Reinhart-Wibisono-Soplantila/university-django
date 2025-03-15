from django.urls import path
from .views import GradeApiView, TermApiView, StatusApiView, FacultyApiView, DepartmentApiView

app_name='app_common'
urlpatterns=[
    path('grade/', GradeApiView.as_view(), name="all grade"),
    path('grade/<int:grade_id>', GradeApiView.as_view(), name='specific grade'),
    
    path('term/', TermApiView.as_view(), name="all term"),
    path('term/<str:term_code>', TermApiView.as_view(), name="specific term"),
    
    path('status/', StatusApiView.as_view(), name="all status"),
    path('status/<int:status_id>', StatusApiView.as_view(), name="specific status"),
        
    path('faculty/', FacultyApiView.as_view(), name='all_faculty'),
    path('faculty/<int:faculty_id>', FacultyApiView.as_view(), name='specific_faculty'),
    
    path('department/', DepartmentApiView.as_view(), name='all_department'),
    path('department/<int:department_id>', DepartmentApiView.as_view(), name='specific_department'),
]