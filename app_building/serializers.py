from rest_framework import serializers
from .models import Building, Room
from app_common.serializers import FacultySerializer
from app_common.models import Faculty
from django.shortcuts import get_object_or_404

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
    
    def create(self, validated_data):
        faculty_id=validated_data.pop("faculty_id", None)
        if faculty_id is None:
            raise serializers.ValidationError({"faculty_id": "Field ini wajib di isi."})
        validated_data["faculty"]=get_object_or_404(Faculty, id=faculty_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        faculty_id=validated_data.pop("faculty_id", None)
        if faculty_id is not None:
            faculty=get_object_or_404(Faculty, id=faculty_id)
            instance.faculty= faculty
        return super().update(instance, validated_data)
    
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
        allow_null=True,
    )
    building=BuildingSerializer(read_only=True)
    class Meta:
        model=Room
        fields='__all__'
        
    def validate_building_id(self, value):
        if not Building.objects.filter(id=value).exists():
            raise serializers.ValidationError("Building dengan Id ini tidak valid")
        return value
    
    def create(self, validated_data):
        building_id=validated_data.pop("building_id", None)
        if building_id is None:
            raise serializers.ValidationError({"building_id": "Field ini wajib diisi."})
        validated_data["building"]=get_object_or_404(Building, id=building_id)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        building_id=validated_data.pop("building_id", None)
        if building_id is not None:
            building=get_object_or_404(Building, id=building_id)
            instance.building= building
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'building' in rep:
            building_data=rep['building']
            building_data.pop('created_at', None)
            building_data.pop('updated_at', None)
            building_data.pop('faculty', None)
        return rep 