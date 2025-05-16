from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django.db import transaction
from .models import *
from app_user.serializer import *
import uuid

# Position & Expertise Serializer
class PositionTeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model=PositionTeachingStaff
        fields='__all__'
        
class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaOfExpertise
        fields='__all__'

# Teachingstaff Serializer
def department_validation(serializer, data):
    faculty = data.get("faculty") or getattr(serializer.instance, 'faculty', None)
    department = data.get("department") or getattr(serializer.instance, 'faculty', None)
    if "faculty" in data and department and not faculty.departments.filter(id=department.id).exists():
        raise ValidationError({"detail": "Department is not listed in this Faculty"})
    return data

# Super Admin Serializer
class SuperAdminSerializer_Get(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model=SuperAdminStaff
        fields='__all__'

class SuperAdminSerializer_Create(serializers.ModelSerializer):
    user = ReadOnlyUsernameUserSerializer()
    full_name=serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model=SuperAdminStaff
        fields=['nip', 'full_name', 'phone_number', 'user']
    
    def validate(self, attrs):
        department_validation(self, attrs)
        return attrs
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        try:
            with transaction.atomic():
                user_data['username'] = f"temp-{uuid.uuid4().hex[:10]}"
                user_data['password'] = f"temp-{uuid.uuid4().hex[:10]}"
                user=User.objects.create_user(**user_data)
                group=Group.objects.get(name='Admin')
                user.groups.add(group)
                superadminstaff = SuperAdminStaff.objects.create(user=user, **validated_data)
                user.username=superadminstaff.nip
                user.set_password(superadminstaff.nip)
                user.save()
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return superadminstaff
    
class SuperAdminSerializer_Update(serializers.ModelSerializer):
    user = UserSerializer()
    date_birth = serializers.DateField(required=True)
    
    class Meta:
        model = SuperAdminStaff
        fields= '__all__'
        read_only_fields=['nip', 'user']
    
    def validate(self, attrs):
        department_validation(self, attrs)
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
            raise ValidationError(f"An error occurred while updating user: {str(e)}")
        return instance

class TeachingStaffSerializer_Get(serializers.ModelSerializer):
    user=UserSerializer()
    
    areas_of_expertise=ExpertiseSerializer(many=True)
    class Meta:
        model=TeachingStaff
        fields='__all__'
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        rep['areas_of_expertise']=[
            {
                'id':areas.id,
                'name':areas.expertise_field
            } for areas in instance.areas_of_expertise.all()
        ]
        return rep

class TeachingStaffSerializer_Create(serializers.ModelSerializer):
    user=ReadOnlyUsernameUserSerializer()
    full_name=serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model=TeachingStaff
        fields=['nip', 'full_name', 'faculty', 'department','position' ,'phone_number', 'user']
    
    def validate(self, data):
        department_validation(self, data)
        return data
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        
        # uncomment group if role flexible (can select more than one or change role)
        # group_data=user_data.pop('groups')
        # group_ids=[group.id for group in group_data]
        try:
            with transaction.atomic():
                user_data['username'] = f"temp-{uuid.uuid4().hex[:10]}"
                user_data['password'] = f"temp-{uuid.uuid4().hex[:10]}"
                user=User.objects.create_user(**user_data)
                
                # uncomment group if role flexible (can select more than one or change role)
                # user.groups.set(group_ids)
                
                # comment this if select can select more than one or change role
                group=Group.objects.get(name='Teaching Staff')
                user.groups.add(group)
                
                teachingstaff=TeachingStaff.objects.create(user=user, **validated_data)
                user.username=teachingstaff.nip
                user.set_password(teachingstaff.nip)
                user.save()
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return teachingstaff
    
class TeachingStaffSerializer_Update(serializers.ModelSerializer):
    user=UserSerializer()
    date_birth = serializers.DateField(required=True)
    
    class Meta:
        model = TeachingStaff
        fields= '__all__'
        read_only_fields=['nip', 'user']
    
    def validate(self, data):
        department_validation(self, data)
        return data
    
    def update(self, instance, validated_data):
        user_data=validated_data.pop('user', None)
        areas_of_expertise_data=validated_data.pop('areas_of_expertise', None)
        try:
            with transaction.atomic():
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()

                if user_data:
                    # group_data=validated_data.pop('groups', None)
                    user=instance.user
                    serializer=UserSerializer(user, data=user_data, partial=True)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                    user.save()
                    
                    # change this if you want make flexible group (more than one)
                    # if group_data is not None and len(group_data)!=1:
                    #     user.groups.set(group_data)    
                        
                if areas_of_expertise_data is not None:
                    instance.areas_of_expertise.set(areas_of_expertise_data)
        except Exception as e:
            raise ValidationError(f"An error occurred while updating user: {str(e)}")
        return instance
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        rep.pop('password', None)
        return rep
    
class AdminStaffSerializer_Get(serializers.ModelSerializer):
    user=UserSerializer()
    
    class Meta:
        model=AdministrativeStaff
        fields='__all__'

class AdminStaffSerializer_Create(serializers.ModelSerializer):
    user=ReadOnlyUsernameUserSerializer()
    full_name=serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model=AdministrativeStaff
        fields=['nip', 'full_name', 'faculty', 'department', 'phone_number', 'user']
    
    def validate(self, data):
        department_validation(self, data)
        return data
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        try:
            with transaction.atomic():
                user_data['username'] = f"temp-{uuid.uuid4().hex[:10]}"
                user_data['password'] = f"temp-{uuid.uuid4().hex[:10]}"
                user=User.objects.create_user(**user_data)
                group=Group.objects.get(name='Administrative Staff')
                user.groups.add(group)
                administrativestaff=AdministrativeStaff.objects.create(user=user, **validated_data)
                user.username=administrativestaff.nip
                user.set_password(administrativestaff.nip)
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return administrativestaff

class AdminStaffSerializer_Update(serializers.ModelSerializer):
    user=UserSerializer()
    date_birth = serializers.DateField(required=True)
    
    class Meta:
        model=AdministrativeStaff
        fields='__all__'
        read_only_fields=['nip', 'user']
        
    def validate(self, data):
        return department_validation(self, data)
    
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
            raise ValidationError(f"An error occurred while updating user: {str(e)}")
        return instance
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        rep.pop('password', None)
        return rep
