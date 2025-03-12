from django.urls import path
from .views import BuildingApiView, RoomApiView, FacultyApiView, DepartmentApiView

app_name="app_building"
url_patterns=[
    path('', BuildingApiView.as_view, name='all_building'),
    path('<int:id>', BuildingApiView.as_view, name='specific_building'),
    
    path('room/', RoomApiView.as_view, name='all_room'),
    path('room/<int:id>', RoomApiView.as_view, name='specific_room'),
    
    path('faculty/', FacultyApiView.as_view, name='all_faculty'),
    path('faculty/<int:id>', FacultyApiView.as_view, name='specific_faculty'),
    
    path('department/', DepartmentApiView.as_view, name='all_department'),
    path('department/<int:id>', DepartmentApiView.as_view, name='specific_department'),
]