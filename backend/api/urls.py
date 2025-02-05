from django.urls import path
from .views import (
    UserListCreate, UserDetail,
    ParentListCreate, ParentDetail,
    StudentListCreate, StudentDetail,
    AdministrationListCreate, AdministrationDetail,
    home  # Add home view import
)

urlpatterns = [
    path('', home, name='home'),  # Add this line for the main page
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user-detail'),
    path('parents/', ParentListCreate.as_view(), name='parent-list-create'),
    path('parents/<int:pk>/', ParentDetail.as_view(), name='parent-detail'),
    path('students/', StudentListCreate.as_view(), name='student-list-create'),
    path('students/<uuid:pk>/', StudentDetail.as_view(), name='student-detail'),
    path('administrations/', AdministrationListCreate.as_view(), name='administration-list-create'),
    path('administrations/<uuid:pk>/', AdministrationDetail.as_view(), name='administration-detail'),
]
