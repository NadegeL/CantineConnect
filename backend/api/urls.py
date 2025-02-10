from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    ParentViewSet, 
    StudentViewSet, 
    AdministrationViewSet, 
    AllergyViewSet,
    SchoolZoneViewSet,
    HolidayViewSet
)

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'parents', ParentViewSet)
router.register(r'students', StudentViewSet)
router.register(r'administration', AdministrationViewSet)
router.register(r'allergies', AllergyViewSet)
router.register(r'school-zones', SchoolZoneViewSet)
router.register(r'holidays', HolidaysViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
