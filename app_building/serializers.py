from rest_framework import serializers
from .models import Building, Room
from app_common.serializers import FacultySerializer
from app_common.models import Faculty
from django.shortcuts import get_object_or_404

# Gabungan untuk Read dan Write method
class BuildingSerializer(serializers.ModelSerializer):
    faculty_id = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(), 
        write_only=True,
        required=False,
        allow_null=True,
        source='faculty',
        error_messages={
        'does_not_exist': 'Faculty dengan ID {pk_value} tidak ditemukan',
        'incorrect_type': 'Faculty ID harus berupa angka'})
    faculty = FacultySerializer(read_only=True)  # Untuk response
    
    class Meta:
        model = Building
        fields = '__all__'
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'faculty' in rep and rep['faculty'] is not None:
            data=rep['faculty']
            data.pop('created_at', None)
            data.pop('updated_at', None)
        return rep
    
class RoomSerializer(serializers.ModelSerializer):
    building_id=serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(),
        write_only=True,
        required=True,
        allow_null=False,
        source='building',
        error_messages={
            'does_not_exist': 'Building dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Building ID harus berupa angka',
            'required': 'Field building_id harus diisi!'}
    )
    building=BuildingSerializer(read_only=True)
    
    class Meta:
        model=Room
        fields='__all__'
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'building' in rep:
            building_data=rep['building']
            building_data.pop('created_at', None)
            building_data.pop('updated_at', None)
            building_data.pop('faculty', None)   #menghapus relasi building dan faculty dari tampilan response
        return rep 