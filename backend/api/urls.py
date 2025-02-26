from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView, current_user, create_initial_admin, RegisterView, LogoutView
from django.contrib.auth.views import LoginView
from .views import LogoutView
from .views import create_initial_admin
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserViewSet,
    ParentViewSet,
    StudentViewSet,
    AdministrationViewSet,
    AddressViewSet,
    SchoolClassViewSet,
    AllergyViewSet,
    SchoolZoneViewSet,
    HolidaysViewSet,
    LogoutView,
    create_initial_admin,
    add_admin,
    home
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'administrations', AdministrationViewSet)
router.register(r'addresses', AddressViewSet)
router.register(r'classes', SchoolClassViewSet)
router.register(r'allergies', AllergyViewSet)
router.register(r'school-zones', SchoolZoneViewSet)
router.register(r'holidays', HolidaysViewSet)

urlpatterns = [
    path('users/me/', views.current_user, name='current-user'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('create-initial-admin/', views.create_initial_admin,
         name='create-initial-admin'),
    path('add-admin/', views.add_admin, name='add-admin'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
]
