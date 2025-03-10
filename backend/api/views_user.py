from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer


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
