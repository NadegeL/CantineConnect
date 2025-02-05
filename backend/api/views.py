from django.shortcuts import render
from rest_framework import generics
from .models import User, Parent, Student, Administration
from .serializers import UserSerializer, ParentSerializer, StudentSerializer, AdministrationSerializer

class UserListCreate(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ParentListCreate(generics.ListCreateAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class ParentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Parent.objects.all()
    serializer_class = ParentSerializer

class StudentListCreate(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AdministrationListCreate(generics.ListCreateAPIView):
    queryset = Administration.objects.all()
    serializer_class = AdministrationSerializer

class AdministrationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administration.objects.all()
    serializer_class = AdministrationSerializer
