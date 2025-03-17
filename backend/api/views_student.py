from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Allergy, StudentAllergy, ParentChildRelation, Parent
from .serializers import (AllergySerializer, StudentSerializer,
                          ParentChildRelationSerializer, StudentSerializer)


@api_view(['POST'])
def create_allergy_for_student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AllergySerializer(data=request.data)
    if serializer.is_valid():
        allergy = serializer.save()
        StudentAllergy.objects.create(student=student, allergy=allergy)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_parent_child_relation(request):
    serializer = ParentChildRelationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_parent_child_relations(request):
    relations = ParentChildRelation.objects.all()
    serializer = ParentChildRelationSerializer(relations, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def update_parent_child_relation(request, relation_id):
    try:
        relation = ParentChildRelation.objects.get(id=relation_id)
        serializer = ParentChildRelationSerializer(relation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except ParentChildRelation.DoesNotExist:
        return Response({"error": "Relation not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_parent_child_relation(request, relation_id):
    try:
        relation = ParentChildRelation.objects.get(id=relation_id)
        relation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except ParentChildRelation.DoesNotExist:
        return Response({"error": "Relation not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_student(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = StudentSerializer(student, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_student_allergies(request, student_id):
    try:
        student = Student.objects.get(pk=student_id)
        allergies = StudentAllergy.objects.filter(
            student=student).select_related('allergy')
        serializer = AllergySerializer(
            [sa.allergy for sa in allergies], many=True)
        return Response(serializer.data)
    except Student.DoesNotExist:
        return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def by_parent(request, parent_id):
    try:
        relations = ParentChildRelation.objects.filter(parent__id=parent_id)
        student_ids = [rel.student.id for rel in relations]
        students = Student.objects.filter(id__in=student_ids)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    except Parent.DoesNotExist:
        return Response({"error": "Parent non trouvé"}, status=404)
