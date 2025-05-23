"""
URL configuration for university project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


def custom_404_handler(request, exception):
    return JsonResponse({
        "status code":404,
        'status':'error',
        "message":'page not found'
    }, status=404)

handler404=custom_404_handler

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('common/', include('app_common.urls', namespace='app_common')),
    path('building/', include('app_building.urls', namespace='app_building')),
    path('student/', include('app_student.urls', namespace='app_student')),
    path('staff/', include('app_staff.urls', namespace='app_staff')),
    path('course/', include('app_course.urls', namespace='app_course')),
    path('schedule/', include('app_schedule.urls', namespace='app_schedule')),
]
