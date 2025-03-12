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
    
    def create(self, validated_data):
        faculty=validated_data['faculty']
        faculty_code=faculty.faculty_code
        last_department=Department.objects.filter(faculty=faculty).order_by('-department_code').first()
        if last_department is not None:
            las_number=int(last_department.department_code[1:])
            new_number=las_number+1
        else:
            new_number=1
        department_code=f"{faculty_code}{new_number:03d}"
        validated_data['department_code']=department_code
        return super().create(validated_data)