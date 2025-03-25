from rest_framework import serializers
from .models import Student
from phonenumber_field.serializerfields import PhoneNumberField

class StudentSerializer(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=Student
        fields='__all__'
        read_only_fields=['nim']