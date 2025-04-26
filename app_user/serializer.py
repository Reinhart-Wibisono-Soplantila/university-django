from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=True)
    
    class Meta:
        model=User
        fields=['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs={
            'username':{'read_only':True},
            'password':{'write_only':True},        
            'first_name': {'allow_blank': False},
            'last_name': {'allow_blank': False},
            }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        action=self.context.get('view').action if 'view' in self.context else None
        if action=="create":
            self.fields['password'].required=False
        elif action=="update":
            for field in self.fields:
                self.fields[field].required=True
    
    def update(self, instance, validated_data):
        password=validated_data.pop('password', None)
        if password:
            instance.set_password(password)
            
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
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

class ReadOnlyUsernameUserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=False)
    first_name = serializers.CharField(allow_blank=True)
    last_name = serializers.CharField(allow_blank=True)
    
    class Meta(UserSerializer.Meta):
        pass