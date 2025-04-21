from rest_framework import serializers
from django.contrib.auth.models import User, Group
from phonenumber_field.serializerfields import PhoneNumberField
from .models import TeachingStaff, PositionTeachingStaff, AdministrativeStaff, AreaOfExpertise, SuperAdminStaff
from rest_framework.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Model User
        fields = ['email', 'username', 'password', 'first_name', 'last_name']
        extra_kwargs = {**{field: {'required': True} for field in fields}, 'password': {'write_only': True}}
    
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # user.is_valid(raise_exception=True)
        instance.save()
        return instance

class SuperAdminSerializer_Get(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=SuperAdminStaff
        fields='__all__'

class SuperAdminSerializer_Regis(serializers.ModelSerializer):
    class Meta:
        model=SuperAdminStaff
        fields=['nip', 'full_name', 'phone_number']

    def validate_nip(self, value):
        if SuperAdminStaff.objects.filter(nip=value).exists():
            raise serializers.ValidationError("NIP must be unique.")
        return value
    
    def validate_phone_number(self, value):
        if TeachingStaff.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number must be unique.")
        return value

class SuperAdminSerializer_Create(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model=SuperAdminStaff
        fields=['nip', 'full_name', 'phone_number', 'user']

    def validate_nip(self, value):
        if SuperAdminStaff.objects.filter(nip=value).exists():
            raise serializers.ValidationError("NIP must be unique.")
        return value
    
    def validate_phone_number(self, value):
        if TeachingStaff.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number must be unique.")
        return value
    
    def create(self, validated_data):
        user_data=validated_data.pop('user')
        try:
            user=User.objects.create_user(**user_data)
            superadminstaff = SuperAdminStaff.objects.create(user=user, **validated_data)
        except Exception as e:
            raise ValidationError(f"An error occurred while creating user: {str(e)}")
        return superadminstaff
    
class SuperAdminSerializer_Update(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model=SuperAdminStaff
        fields=['nip', 'full_name', 'phone_number', 'user']

    def validate_nip(self, value):
        if SuperAdminStaff.objects.filter(nip=value).exists():
            raise serializers.ValidationError("NIP must be unique.")
        return value
    
    def validate_phone_number(self, value):
        if TeachingStaff.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Phone number must be unique.")
        return value
    
    def update(self, instance, validated_data):
        user_data=validated_data.pop('user', None)
        
        try:
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
    
class AdminStaffSerializer(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=AdministrativeStaff
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

#Validate data that is not link to User or user profile 
class PositionTeachingSerializer(serializers.ModelSerializer):
    class Meta:
        model=PositionTeachingStaff
        fields='__all__'
        
class ExpertiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=AreaOfExpertise
        fields='__all__'