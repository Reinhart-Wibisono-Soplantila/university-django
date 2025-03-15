from rest_framework import serializers
from .models import Student
from phonenumber_field.serializerfields import PhoneNumberField

class StudentSerializer(serializers.Serializer):
    phone_number=PhoneNumberField()
    
    class Meta:
        model=Student
        fields='__all__'