from rest_framework import viewsets
from .models import User, Parent, Student, Administration
from .serializers import UserSerializer, ParentSerializer, StudentSerializer, AdministrationSerializer
from drf_yasg.utils import swagger_auto_schema
import datetime
from django.http import HttpResponse
from django.shortcuts import redirect

def home(request):
    return HttpResponse("Welcome to the CantineConnect API")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        request_body=UserSerializer,
        operation_description="Create a new user",
        operation_summary="Create a user",
        responses={201: UserSerializer()},
        examples={
            'application/json': {
                'email': 'user@example.com',
                'first_name': 'John',
                'last_name': 'Doe',
                'is_active': True,
                'is_superuser': False,
                'is_staff': True,
                'username': 'john_doe',
                'password': 'securepassword123',
                'last_login': datetime.datetime.now().isoformat(),
                'date_joined': datetime.datetime.now().isoformat(),
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class ParentViewSet(viewsets.ModelViewSet):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

    @swagger_auto_schema(
        request_body=ParentSerializer,
        operation_description="Create a new parent",
        operation_summary="Create a parent",
        responses={201: ParentSerializer()},
        examples={
            'application/json': {
                'email': 'parent@example.com',
                'phone_number': '0123456789',
                'is_admin': False,
                'invoice_available': True,
                'address': {
                    'address_line_1': '123 Rue de la Paix',
                    'address_line_2': 'Appartement 4',
                    'city': 'Paris',
                    'postal_code': '75000',
                    'country': 'France'
                }
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    @swagger_auto_schema(
        request_body=StudentSerializer,
        operation_description="Create a new student",
        operation_summary="Create a student",
        responses={201: StudentSerializer()},
        examples={
            'application/json': {
                'birth_date': '2010-01-01',
                'grade': 'CM2',
                'parent': 1
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class AdministrationViewSet(viewsets.ModelViewSet):
    queryset = Administration.objects.all()
    serializer_class = AdministrationSerializer

    @swagger_auto_schema(
        request_body=AdministrationSerializer,
        operation_description="Create a new administration",
        operation_summary="Create an administration",
        responses={201: AdministrationSerializer()},
        examples={
            'application/json': {
                'email': 'admin@example.com',
                'is_admin': True,
                'invoice_edited': False,
                'address': {
                    'address_line_1': '123 Rue de la Paix',
                    'address_line_2': 'Appartement 4',
                    'city': 'Paris',
                    'postal_code': '75000',
                    'country': 'France'
                },
                'zone_id': 'Z123'
            }
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
