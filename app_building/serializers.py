from rest_framework import serializers
from .models import Building, Room, Faculty, Department

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model=Building
        fields='__all__'

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields='__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model=Faculty
        fields='__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'