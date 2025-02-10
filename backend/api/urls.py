from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ParentViewSet, StudentViewSet, AdministrationViewSet, AddressViewSet, home

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'administrations', AdministrationViewSet)
router.register(r'addresses', AddressViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('', include(router.urls)),
]
