from django.urls import path
from .views import BuildingApiView, RoomApiView, FacultyApiView, DepartmentApiView

app_name='app_building'
urlpatterns=[
    path('', BuildingApiView.as_view(), name='all_building'),
    path('<int:building_id>', BuildingApiView.as_view(), name='specific_building'),
    
    path('room/', RoomApiView.as_view(), name='all_room'),
    path('room/<int:room_id>', RoomApiView.as_view(), name='specific_room'),
    
    path('faculty/', FacultyApiView.as_view(), name='all_faculty'),
    path('faculty/<int:faculty_id>', FacultyApiView.as_view(), name='specific_faculty'),
    
    path('department/', DepartmentApiView.as_view(), name='all_department'),
    path('department/<int:department_id>', DepartmentApiView.as_view(), name='specific_department'),
]