from rest_framework import serializers
from .models import User, Parent, Student, Administration

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
        extra_kwargs = {
            'password': {'write_only': True}#password is write only
        }

class ParentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    address = AddressSerializer()
    
    class Meta:
        model = Parent
        fields = '__all__'
        
    def create(self, validated_data):#create a new parent
        user_data = validated_data.pop('user')
        address_data = validated_data.pop('address')
        user = User.objects.create(**user_data)
        address = Address.objects.create(**address_data)
        parent = Parent.objects.create(user=user, address=address, **validated_data)
        return parent

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    parents = ParentSerializer(many=True)
    allergies = AllergySerializer(many=True)
    
    class Meta:
        model = Student
        fields = '__all__'

class AdministrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administration
        fields = '__all__'
        
class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
        
class AllergySerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergy
        fields = '__all__'
class SchoolZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolZone
        fields = '__all__'
        
class HolidaySerializer(serializers.ModelSerializer):
    zone = SchoolZoneSerializer()
    
    class Meta:
        model = Holiday
        fields = '__all__'
        
    def create(self, validated_data):
        zone_data = validated_data.pop('zone')
        zone = SchoolZone.objects.create(**zone_data)
        holidays = Holiday.objects.create(zone=zone, **validated_data)
        return holidays
