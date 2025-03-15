from rest_framework import serializers
from .models import TeachingStaff, PositionTeachingStaff, AdministrativeStaff

class TeachingStaffSerializer(serializers.Serializer):
    class Meta:
        model=TeachingStaff
        fields='__all__'
        
class PositionTeachingSerializer(serializers.Serializer):
    class Meta:
        model=PositionTeachingStaff
        fields='__all__'
    
class AdminStaffSerializer(serializers.Serializer):
    class Meta:
        model=AdministrativeStaff
        fields='__all__'