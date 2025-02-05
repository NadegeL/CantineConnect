from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from api.views import (
    UserListCreate, UserDetail,
    ParentListCreate, ParentDetail,
    StudentListCreate, StudentDetail,
    AdministrationListCreate, AdministrationDetail
)

schema_view = get_schema_view(
    openapi.Info(
        title="CantineConnect API",
        default_version='v1',
        description="API documentation for CantineConnect",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
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
    path('api/', include('api.urls')),  # Make sure this line includes your API URLs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
