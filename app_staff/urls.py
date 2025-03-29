from django.urls import path
from .views import *

app_name='app_staff'
urlpatterns = [
    path('teaching-staff/', TeachingStaffApiView.as_view(), name='teaching_staff'),
    path('teaching-staff/<str:nip>', TeachingStaffApiView.as_view(), name='teaching_staff'),
    path('admin-staff/', AdministrativeStaffApiView.as_view(), name='admin_staff'),
    path('admin-staff/<int:nip>', AdministrativeStaffApiView.as_view(), name='admin_staff'),
    path('position-staff/', TeachingPositionApiView.as_view(), name='position_staff'),
    path('position-staff/<int:position_id>', TeachingPositionApiView.as_view(), name='position_staff'),   
    path('expertise/', ExpertiseApiView.as_view(), name='all_expertise'),
    path('expertise/<int:expertise_id>', ExpertiseApiView.as_view(), name='specific_expertise'),   
]