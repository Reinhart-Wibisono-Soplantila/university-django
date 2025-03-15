from rest_framework import serializers
from .models import TeachingStaff, PositionTeachingStaff

class TeachingStaffSerializer(serializers.Serializer):
    class Meta:
        model=TeachingStaff
        fields='__all__'
        
class PositionTeachingSerializer(serializers.Serializer):
    class Meta:
        model=PositionTeachingStaff
        fields='__all__'