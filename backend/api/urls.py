from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from django.contrib.auth.views import LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from .views import StudentViewSet
from .views_user import current_user, create_initial_admin, add_admin
from .views_allergy import create_allergy_for_student, delete_student_allergy, update_allergy
from .views_student import (create_parent_child_relation, list_parent_child_relations,
                            update_parent_child_relation, delete_parent_child_relation, update_student)

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
    path('users/me/', current_user, name='current-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    path('create-initial-admin/', create_initial_admin,
         name='create-initial-admin'),
    path('add-admin/', add_admin, name='add-admin'),
    path('parent/profile/', ParentProfileView.as_view(), name='parent-profile'),
    path('students/<int:student_id>/allergies/create/',
         create_allergy_for_student, name='create-allergy-for-student'),
    path('students/<int:student_id>/', update_student, name='update-student'),
    path('students/<int:student_id>/allergies/<int:allergy_id>/',
         delete_student_allergy, name='delete-student-allergy'),
    path('allergies/<int:allergy_id>/', update_allergy, name='update-allergy'),
    path('parent-child-relations/', create_parent_child_relation,
         name='create-parent-child-relation'),
    path('parent-child-relations/list/', list_parent_child_relations,
         name='list-parent-child-relations'),
    path('parent-child-relations/<int:relation_id>/',
         update_parent_child_relation, name='update-parent-child-relation'),
    path('parent-child-relations/<int:relation_id>/delete/',
         delete_parent_child_relation, name='delete-parent-child-relation'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(), name='login'),
]
