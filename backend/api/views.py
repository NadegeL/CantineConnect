from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import (User, Parent, Student, Administration, 
                    Allergy, SchoolZone, Holidays)
from .serializers import (UserSerializer, ParentSerializer, StudentSerializer, 
                         AdministrationSerializer, AllergySerializer, 
                         SchoolZoneSerializer, HolidaysSerializer)
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
    
class AllergyViewSet(viewsets.ModelViewSet):
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializer

    @swagger_auto_schema(
        operation_description="Liste toutes les allergies",
        operation_summary="Liste des allergies",
        responses={200: AllergySerializer(many=True)}
    )
    def list(self, request):
        return super().list(request)

    @action(detail=True, methods=['get'])
    def students_with_allergy(self, request, pk=None):
        """Obtenir tous les étudiants ayant une allergie spécifique"""
        try:
            allergy = self.get_object()
            students = Student.objects.filter(allergies=allergy)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class SchoolZoneViewSet(viewsets.ModelViewSet):
    queryset = SchoolZone.objects.all()
    serializer_class = SchoolZoneSerializer

    @action(detail=True, methods=['get'])
    def get_holidays(self, request, pk=None):
        """Obtenir toutes les vacances pour une zone spécifique"""
        try:
            zone = self.get_object()
            holidays = Holidays.objects.filter(zone=zone)
            serializer = HolidaysSerializer(holidays, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

class HolidaysViewSet(viewsets.ModelViewSet):
    queryset = Holidays.objects.all()
    serializer_class = HolidaysSerializer

    @action(detail=False, methods=['get'])
    def current_holidays(self, request):
        """Obtenir les vacances en cours"""
        today = datetime.date.today()
        current_holidays = Holidays.objects.filter(
            start_date__lte=today,
            end_date__gte=today
        )
        serializer = self.get_serializer(current_holidays, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def upcoming_holidays(self, request):
        """Obtenir les prochaines vacances"""
        today = datetime.date.today()
        upcoming = Holidays.objects.filter(
            start_date__gt=today
        ).order_by('start_date').first()
        if upcoming:
            serializer = self.get_serializer(upcoming)
            return Response(serializer.data)
        return Response(
            {'message': 'Pas de vacances prévues'}, 
            status=status.HTTP_404_NOT_FOUND
        )
