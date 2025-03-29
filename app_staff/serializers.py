from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import TeachingStaff, PositionTeachingStaff, AdministrativeStaff, AreaOfExpertise
from rest_framework.exceptions import ValidationError

class TeachingStaffSerializer(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=TeachingStaff
        fields='__all__'
    
    def validate_phone_number(self, value):
        if TeachingStaff.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number must be unique.")
        return value
    
    def validate(self, data):
        faculty = data.get("faculty") or self.instance.faculty
        department = data.get("department") or self.instance.department
        if "faculty" in data and department and not faculty.departments.filter(id=department.id).exists():
            raise ValidationError({"detail": "Department is not listed in this Faculty"})
        return data
        
class PositionTeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model=PositionTeachingStaff
        fields='__all__'
    
class AdminStaffSerializer(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=AdministrativeStaff
        fields='__all__'

class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaOfExpertise
        fields='__all__'