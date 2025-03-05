from django.contrib.auth import get_user_model
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import (Address, Administration, Allergy, Holidays, Parent,
                     SchoolClass, SchoolZone, Student)


User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data['user_type'] = self.user.user_type
        return data


class UserSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(write_only=True, required=False)
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name',
                  'last_name', 'user_type', 'new_password']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user_type = validated_data.get('user_type')
        if user_type == 'school_admin':
            validated_data['is_staff'] = True
        user = User.objects.create_user(**validated_data)

        if user_type == 'parent':
            Parent.objects.create(user=user)

        return user

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field is mandatory.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("This field is mandatory.")
        return value


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address_line_1', 'address_line_2',
                  'city', 'postal_code', 'country']


class AdministrationSerializer(serializers.ModelSerializer):
    zone = serializers.CharField()

    class Meta:
        model = Administration
        fields = ['invoice_edited', 'zone']


class ParentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parent
        fields = ['user', 'phone_number', 'invoice_available',
                  'address', 'is_activated', 'relation']


class RegisterSerializer(serializers.ModelSerializer):
    address = AddressSerializer(required=False)
    administration = AdministrationSerializer(required=False)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name',
                  'user_type', 'address', 'administration']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        administration_data = validated_data.pop('administration', None)
        user_type = validated_data.get('user_type')

        user = User.objects.create_user(**validated_data)

        if address_data:
            address = Address.objects.create(**address_data)
            user.address = address
            user.save()

        if administration_data:
            zone_name = administration_data.pop('zone')
            zone, _ = SchoolZone.objects.get_or_create(name=zone_name)
            Administration.objects.create(
                user=user, address=address, zone=zone, **administration_data)

        if user_type == 'parent':
            Parent.objects.create(user=user)

        return user


class ParentProfileUpdateSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer()

    class Meta:
        model = Parent
        fields = ['phone_number', 'invoice_available', 'address',
                  'user', 'relation']

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        user_data = validated_data.pop('user', None)

        if address_data:
            address = instance.address
            if address:
                for attr, value in address_data.items():
                    setattr(address, attr, value)
                address.save()
            else:
                address = Address.objects.create(**address_data)
                instance.address = address

        if user_data:
            user = instance.user
            for attr, value in user_data.items():
                setattr(user, attr, value)
            user.save()

        if 'relation' in validated_data:
            instance.relation = validated_data['relation']

        return super().update(instance, validated_data)


class SchoolZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolZone
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


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = '__all__'


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'


class HolidaysSerializer(serializers.ModelSerializer):
    zone = SchoolZoneSerializer()

    class Meta:
        model = Holidays
        fields = '__all__'

    def create(self, validated_data):
        zone_data = validated_data.pop('zone')
        zone, _ = SchoolZone.objects.get_or_create(**zone_data)
        holidays = Holidays.objects.create(zone=zone, **validated_data)
        return holidays
