from rest_framework import serializers
from django.contrib.auth.models import User, Group
from phonenumber_field.serializerfields import PhoneNumberField
from .models import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import transaction

# Position & Expertise Serializer
class PositionTeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model=PositionTeachingStaff
        fields='__all__'
        
class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaOfExpertise
        fields='__all__'
        
# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # groups= serializers.PrimaryKeyRelatedField(
    #     queryset=Group.objects.all(),
    #     many=False,
    #     required=True,
    #     allow_empty=False,
    #     write_only=True
    # )
    class Meta:
        model = User  # Model User
        # fields = ['email', 'username', 'password', 'first_name', 'last_name', 'groups']
        fields = ['email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
    
    # def validate_groups(self, value):
    #     if not value:
    #         raise serializers.ValidationError("group required")
    #     if (isinstance(value, list)) and len(value)!=1:
    #         raise serializers.ValidationError("Exactly one group must be selected.")    
    #     return value
    
    def validate_email(self, value):
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError("Wrong email address")
        
        filter_email=User.objects.filter(email=value)
        if self.instance:
            if filter_email.exclude(id=self.instance.id).exists(): 
                raise ValidationError("User with this email already exist")
        if filter_email.exists():
            raise ValidationError("User with this email already exist")
        return value 
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # user.is_valid(raise_exception=True)
        instance.save()
        return instance
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        rep['groups']=[
            {
                'id':group.id,
                'name':group.name
                }for group in instance.groups.all()]
        return rep
    
# Super Admin Serializer
class SuperAdminSerializer_Get(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    user = UserSerializer()
    class Meta:
        model=SuperAdminStaff
        fields='__all__'

class SuperAdminSerializer_Create(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model=SuperAdminStaff
        fields=['nip', 'full_name', 'phone_number', 'user']
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        try:
            with transaction.atomic():
                user=User.objects.create_user(**user_data)
                group=Group.objects.get(name='admin')
                user.groups.add(group)
                superadminstaff = SuperAdminStaff.objects.create(user=user, **validated_data)
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return superadminstaff
    
class SuperAdminSerializer_Update(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = SuperAdminStaff
        fields = ['nip', 'full_name', 'phone_number', 'address', 'user']
    
    def update(self, instance, validated_data):
        user_data=validated_data.pop('user', None)
        try:
            with transaction.atomic():
                for attr, value in validated_data.items():
                    setattr(instance, attr, value)
                instance.save()
                
                if user_data:
                    user=instance.user
                    for attr, value in user_data.items():
                        if attr=='password':
                            user.set_password(value)
                        else:
                            setattr(user, attr, value)
                    user.save()
        except Exception as e:
            raise ValidationError(f"An error occurred while updating user: {str(e)}")
        return instance

# Teachingstaff Serializer
def department_validation(serializer, data):
    faculty = data.get("faculty") or getattr(serializer.instance, 'faculty', None)
    department = data.get("department") or getattr(serializer.instance, 'faculty', None)
    if "faculty" in data and department and not faculty.departments.filter(id=department.id).exists():
        raise ValidationError({"detail": "Department is not listed in this Faculty"})
    return data

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
    phone_number=PhoneNumberField()
    user=UserSerializer()
    class Meta:
        model=TeachingStaff
        fields=['nip', 'full_name', 'faculty', 'department','position' ,'phone_number', 'user']
    
    def validate(self, data):
        return department_validation(self, data)
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        
        # uncomment group if role flexible (can select more than one or change role)
        # group_data=user_data.pop('groups')
        # group_ids=[group.id for group in group_data]
        try:
            with transaction.atomic():
                user=User.objects.create_user(**user_data)
                
                # uncomment group if role flexible (can select more than one or change role)
                # user.groups.set(group_ids)
                
                # comment this if select can select more than one or change role
                group=Group.objects.get(name='teaching_staff')
                user.groups.add(group)
                
                teachingstaff=TeachingStaff.objects.create(user=user, **validated_data)
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return teachingstaff
    
class TeachingStaffSerializer_Update(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    user=UserSerializer()
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True, required=True)

    class Meta:
        model = TeachingStaff
        fields= '__all__'
    
    def validate(self, data):
        return department_validation(self, data)
    
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
                    for attr, value in user_data.items():
                        if attr=='password':
                            user.set_password(value)
                        else:
                            setattr(user, attr, value)
                    user.save()
                    
                    # change this if you want make flexible group (more than one)
                    # if group_data is not None and len(group_data)!=1:
                    #     user.groups.set(group_data)    
                        
                if areas_of_expertise_data is not None:
                    instance.areas_of_expertise.set(areas_of_expertise_data)
        except Exception as e:
            raise ValidationError(f"An error occurred while updating user: {str(e)}")
        return instance
    
class AdminStaffSerializer_Get(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    user=UserSerializer()
    class Meta:
        model=AdministrativeStaff
        fields='__all__'

class AdminStaffSerializer_Create(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    user=UserSerializer()
    class Meta:
        model=AdministrativeStaff
        fields=['nip', 'full_name', 'faculty', 'department', 'phone_number', 'user']
    
    def validate(self, data):
        return department_validation(self, data)
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        try:
            with transaction.atomic():
                user=User.objects.create_user(**user_data)
                group=Group.objects.get(name='administrative staff')
                user.groups.add(group)
                administrativestaff=AdministrativeStaff.objects.create(user=user, **validated_data)
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return administrativestaff

class AdminStaffSerializer_Update(serializers.ModelSerializer):
    user=UserSerializer()
    
    class Meta:
        model=AdministrativeStaff
        fields='__all__'
    
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
                    for attr, value in user_data.items():
                        if attr=='password':
                            user.set_password(value)
                        else:
                            setattr(user, attr, value)
                    user.save()
                    
        except Exception as e:
            raise ValidationError(f"An error occurred while updating user: {str(e)}")
        return instance
