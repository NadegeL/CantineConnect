"""
URL configuration for cantineconnect project.

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
from django.urls import path
from .views import (
    UserListCreate, UserDetail,
    ParentListCreate, ParentDetail,
    StudentListCreate, StudentDetail,
    AdministrationListCreate, AdministrationDetail
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user-detail'),
    path('parents/', ParentListCreate.as_view(), name='parent-list-create'),
    path('parents/<int:pk>/', ParentDetail.as_view(), name='parent-detail'),
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('students/<uuid:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('administrations/', AdministrationListCreate.as_view(), name='administration-list-create'),
    path('administrations/<uuid:pk>/', AdministrationDetail.as_view(), name='administration-detail'),
]
