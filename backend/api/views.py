# views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .imports import *
from .app_imports import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import (User, Parent, Student, Administration, Address,
                     SchoolClass, Allergy, SchoolZone, Holidays)
from .serializers import (UserSerializer, ParentSerializer, StudentSerializer,
                          AdministrationSerializer, AddressSerializer,
                          SchoolClassSerializer, AllergySerializer,
                          SchoolZoneSerializer, HolidaysSerializer,
                          RegisterSerializer, ParentProfileUpdateSerializer)
from .services.holidays_service import HolidaysService
import datetime
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()


def home(request):
    return HttpResponse("Bienvenue sur CantineConnect !")


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    if request.user.is_authenticated:
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_initial_admin(request):
    if User.objects.filter(is_staff=True, user_type='school_admin').exists():
        return Response({"error": "Un administrateur du site existe déjà."}, status=403)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_staff=True, user_type='school_admin')
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_admin(request):
    if not request.user.is_staff:
        return Response({"error": "Vous n'avez pas les droits pour ajouter un administrateur."}, status=403)

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save(is_staff=True)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        method='post',
        operation_description="Envoi d'un mot de passe temporaire à un parent",
        operation_summary="Envoi mot de passe temporaire",
        request_body=serializers.Serializer({
            'email': serializers.EmailField(help_text="Email du parent")
        }),
        responses={
            200: serializers.Serializer({'message': serializers.CharField()}),
            403: serializers.Serializer({'error': serializers.CharField()}),
            400: serializers.Serializer({'error': serializers.CharField()})
        }
    )
    @action(detail=False, methods=['post'])
    def send_temporary_password(self, request):
        """envoi du mot de passe temporaire à un parent"""
        if not request.user.is_staff:
            return Response(
                {"error": "accès refusé"},
                status=status.HTTP_403_FORBIDDEN
            )
        email = request.data.get('email')
        if not email:
            return Response(
                {"error": "email requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # générer password provisoire
        temp_password = ''.join(random.choices(
            string.ascii_letters + string.digits, k=10))

        try:
            # créer ou mettre à jour l'utilisateur
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'username': email,
                    'is_active': True,
                    'first_time_login': True
                }
            )
            user.set_password(temp_password)
            user.save()

            send_mail(
                'Voici vos identifiants pour CantineConnect',
                f'''Bonjour,
                Veuillez trouver vos identifiants pour vous connecter à CantineConnect:
                Email: {email}
                Mot de passe: {temp_password}

                À votre première connexion, vous serez invité à changer votre mot de passe.

                Cordialement,
                L'équipe CantineConnect''',
                'noreply@cantineconnect.fr',
                [email],
                fail_silently=False
            )

            return Response({
                "message": f"Mot de passe provisoire envoyé à {email}"
            })
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @swagger_auto_schema(
        method='post',
        operation_description="Changer le mot de passe d'un utilisateur",
        operation_summary="Changer mot de passe",
        request_body=serializers.Serializer({
            'new_password': serializers.CharField(help_text="Nouveau mot de passe"),
            'confirm_password': serializers.CharField(help_text="Confirmation du mot de passe")
        }),
        responses={
            200: serializers.Serializer({'message': serializers.CharField()}),
            403: serializers.Serializer({'error': serializers.CharField()}),
            400: serializers.Serializer({'error': serializers.CharField()})
        }
    )
    @action(detail=False, methods=['post'])
    def change_password_first_login(self, request):
        """Création du mot de passe pour la première connexion"""
        user = request.user
        if not user.first_time_login:
            return Response(
                {"error": "Ce n'est pas votre première connexion"},
                status=status.HTTP_400_BAD_REQUEST
            )

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response(
                {"error": "Les deux champs de mot de passe sont requis"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if new_password != confirm_password:
            return Response(
                {"error": "Les mots de passe ne correspondent pas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # valider password
            validate_password(new_password, user)

            # changer le mot de passe
            user.set_password(new_password)
            user.first_time_login = False
            user.save()

            return Response({
                "message": "Mot de passe changé avec succès"
            })
        except ValidationError as e:
            return Response(
                {"error": list(e.messages)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        print("Requête reçue pour l'enregistrement:", request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ParentProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ParentProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.parent_profile


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
                'zone': 'A'
            }
        }
    )
    def create(self, request, *args, **kwargs):
        if Administration.objects.exists():
            return Response({"error": "Un administrateur existe déjà."}, status=status.HTTP_403_FORBIDDEN)
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class SchoolClassViewSet(viewsets.ModelViewSet):
    queryset = SchoolClass.objects.all()
    serializer_class = SchoolClassSerializer


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
    permission_classes = [AllowAny]
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

    @action(detail=False, methods=['post'])
    def sync_with_api(self, request):
        """Synchronise avec data.gouv.fr"""
        try:
            service = HolidaysService()
            for zone_choice in SchoolZone.ZONE_CHOICES:
                zone_code = zone_choice[0]
                zone = SchoolZone.objects.get(name=zone_code)
                holidays = service.get_holidays(zone=zone_code)

                for holiday_data in holidays:
                    Holidays.objects.update_or_create(
                        zone=zone,
                        start_date=holiday_data['start_date'],
                        end_date=holiday_data['end_date'],
                        defaults={
                            'description': holiday_data['description'],
                            'school_year': holiday_data['school_year']
                        }
                    )

            return Response({"message": "Synchronisation réussie"})
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Veuillez fournir un email et un mot de passe.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response({'error': 'Identifiants invalides.'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Ce compte est désactivé.'}, status=status.HTTP_403_FORBIDDEN)

        user_type = 'unknown'
        token = None

        if user.groups.filter(name='Parent').exists():
            user_type = 'parent'
            token = RefreshToken.for_user(user)
        elif user.groups.filter(name='Administration du Site').exists():
            user_type = 'school_admin'
            token = RefreshToken.for_user(user)
        elif user.is_superuser and user.groups.filter(name='Administrateur du TDB de Django').exists():
            user_type = 'django_admin'
            token = RefreshToken.for_user(user)
        else:
            return Response({'error': 'Groupe utilisateur non reconnu.'}, status=status.HTTP_403_FORBIDDEN)

        if token is None:
            return Response({'error': 'Erreur lors de la génération du token.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        token['user_type'] = user_type
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return Response({
            'access': str(token.access_token),
            'refresh': str(token),
            'user_type': user_type,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }, status=status.HTTP_200_OK)
