from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Student, Allergy, StudentAllergy
from .serializers import AllergySerializer


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


@api_view(['DELETE'])
def delete_student_allergy(request, student_id, allergy_id):
    try:
        student = Student.objects.get(pk=student_id)
        allergy = Allergy.objects.get(pk=allergy_id)
        student_allergy = StudentAllergy.objects.get(
            student=student, allergy=allergy)
        student_allergy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except (Student.DoesNotExist, Allergy.DoesNotExist, StudentAllergy.DoesNotExist):
        return Response({"error": "Student, allergy, or association not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def update_allergy(request, allergy_id):
    try:
        allergy = Allergy.objects.get(pk=allergy_id)
    except Allergy.DoesNotExist:
        return Response({"error": "Allergy not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = AllergySerializer(allergy, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
