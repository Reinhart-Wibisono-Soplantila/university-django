from django.urls import path
from .views import GradeApiView, TermApiView, StatusApiView

app_name='app_common'
urlpatterns=[
    path('grade/', GradeApiView.as_view(), name="all grade"),
    path('grade/<int:grade_id>', GradeApiView.as_view(), name='specific grade'),
    
    path('term/', TermApiView.as_view(), name="all term"),
    path('term/<int:term_id>', TermApiView.as_view(), name="specific term"),
    
    path('status/', StatusApiView.as_view(), name="all status"),
    path('status/<int:status_id>', StatusApiView.as_view(), name="specific status"),
]