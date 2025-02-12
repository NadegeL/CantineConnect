from rest_framework import serializers
from .models import (User, Parent, Student, Administration, Address,
                     SchoolClass, Allergy, SchoolZone, Holidays)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name',
                  'password', 'is_active', 'is_staff', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class ParentSerializer(serializers.ModelSerializer):
    relation = serializers.CharField(
        max_length=50, required=False, allow_blank=True)

    class Meta:
        model = Parent
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    parents = serializers.PrimaryKeyRelatedField(
        queryset=Parent.objects.all(), many=True)
    allergies = serializers.PrimaryKeyRelatedField(
        queryset=Allergy.objects.all(), many=True, required=False)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        parents_data = validated_data.pop('parents', [])
        allergies_data = validated_data.pop('allergies', [])

        student = Student.objects.create(**validated_data)
        student.parents.set(parents_data)
        student.allergies.set(allergies_data)
        return student


class AdministrationSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Administration
        fields = '__all__'

    def validate_user(self, value):
        if not value.is_staff:
            raise serializers.ValidationError(
                "The user must have staff status to be an administrator.")
        return value

    def create(self, validated_data):
        user = validated_data.pop('user')
        administration = Administration.objects.create(
            user=user, **validated_data)
        return administration


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'

class SchoolZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolZone
        fields = '__all__'


class AdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administration
        fields = '__all__'


class HolidaysSerializer(serializers.ModelSerializer):
    zone = SchoolZoneSerializer()

    class Meta:
        model = Holidays
        fields = '__all__'

    def create(self, validated_data):
        zone_data = validated_data.pop('zone')
        zone = SchoolZone.objects.create(**zone_data)
        holidays = Holidays.objects.create(zone=zone, **validated_data)
        return holidays