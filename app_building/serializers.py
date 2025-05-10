from rest_framework import serializers
from .models import Building, Room
from app_common.serializers import FacultySerializer
from app_common.models import Faculty

# Gabungan untuk Read dan Write method
class BuildingSerializer(serializers.ModelSerializer):
    faculty_id = serializers.IntegerField(
        write_only=True,
        required=False,
        allow_null=True,
    )
    faculty = FacultySerializer(read_only=True)  # Untuk response
    
    class Meta:
        model = Building
        fields = '__all__'
        
    def validate_faculty_id(self, value):
        if not Faculty.objects.filter(id=value).exists():
            raise serializers.ValidationError("Faculty dengan ID ini tidak valid")
        return value

    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'faculty' in rep and rep['faculty'] is not None:
            data=rep['faculty']
            data.pop('created_at', None)
            data.pop('updated_at', None)
        return rep
    
class RoomSerializer(serializers.ModelSerializer):
    building_id=serializers.IntegerField(
        write_only=True,
        required=False,
        allow_null=False,
    )
    building=BuildingSerializer(read_only=True)
    class Meta:
        model=Room
        fields='__all__'
        
    def validate_building_id(self, value):
        if value is None:
            return None
        if not Building.objects.filter(id=value).exists():
            raise serializers.ValidationError("Building dengan Id ini tidak valid")
        return value
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'building' in rep:
            building_data=rep['building']
            building_data.pop('created_at', None)
            building_data.pop('updated_at', None)
            building_data.pop('faculty', None)
        return rep 