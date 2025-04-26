from rest_framework import serializers
from .models import Student
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.models import User, Group
from app_user.serializer import *
import uuid

def validation_departments(serializer, data):
    faculty = data.get("faculty") or serializer.instance.faculty
    department = data.get("department") or serializer.instance.department
    if "faculty" in data and department and not faculty.departments.filter(id=department.id).exists():
        raise ValidationError({"detail": "Department is not listed in this Faculty"})

class StudentSerializer_Get(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    user=UserSerializer()
    class Meta:
        model=Student
        fields='__all__'
    
class StudentSerializer_Create(serializers.ModelSerializer):    
    user=ReadOnlyUsernameUserSerializer()
    full_name=serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Student
        fields = ['nim', 'full_name', 'faculty', 'department', 'phone_number', 'registration_year', 'user']
        read_only_fields = ['nim']
    
    # perbaiki nama validate
    def validate(self, attrs):
        validation_departments(self, attrs)
        return attrs

    def create(self, validated_data):
        user_data=validated_data.pop('user')
        try:
            with transaction.atomic():
                user_data['username'] = f"temp-{uuid.uuid4().hex[:10]}"
                user_data['password'] = f"temp-{uuid.uuid4().hex[:10]}"
                user=User.objects.create_user(**user_data)
                group=Group.objects.get(name='Student')
                user.groups.add(group)
                student=Student.objects.create(user=user, **validated_data)
                user.username=student.nim
                user.set_password(student.nim)
                user.save()
        except Exception as e:
            raise ValidationError(f"An error occured while creating user: {str(e)}")
        return student

class StudentSerializer_Update(serializers.ModelSerializer):    
    user=UserSerializer()
    date_birth = serializers.DateField(required=True)
    
    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['nim', 'faculty', 'department', 'user']
    
    def validate(self, attrs):
        validation_departments(self, attrs)
        return attrs
    
    def update(self, instance, validated_data):
        user_data=validated_data.pop('user', None)
        try:
            with transaction.atomic():
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                
                if user_data:
                    user=instance.user
                    serializer=UserSerializer(user, data=user_data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
        except Exception as e:
            raise ValidationError(f"An error occured while updating user: {str(e)}")
        return instance

    def to_representation(self, instance):
        rep=super().to_representation(instance)
        rep.pop('password', None)
        return rep