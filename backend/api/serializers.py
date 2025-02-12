from rest_framework import serializers
from .models import User, Parent, Student, Administration, Address, Allergy, SchoolZone, Holidays


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True}  # password is write only
        }


class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()

    class Meta:
        model = Parent
        fields = '__all__'

    def create(self, validated_data):  # create a new parent
        user_data = validated_data.pop('user')
        address_data = validated_data.pop('address')
        user = User.objects.create(**user_data)
        address = Address.objects.create(**address_data)
        parent = Parent.objects.create(
            user=user, address=address, **validated_data)
        return parent


class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    parents = ParentSerializer(many=True)
    allergies = AllergySerializer(many=True)

    class Meta:
        model = Student
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        parents_data = validated_data.pop('parents')
        allergies_data = validated_data.pop('allergies')
        
        # Créer l'utilisateur
        user = User.objects.create(**user_data)
        
        # Créer l'étudiant
        student = Student.objects.create(user=user, **validated_data)
        
        # Ajouter les parents
        for parent_data in parents_data:
            student.parents.add(parent_data)
            
        # Ajouter les allergies
        for allergy_data in allergies_data:
            student.allergies.add(allergy_data)
            
        return student

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
