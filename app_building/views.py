from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import success_response, created_response, options_response, delete_reponse, error_400_response
from .models import Building, Room, Faculty, Department
from .serializers import BuildingSerializer, RoomSerializer, FacultySerializer, DepartmentSerializer
# Create your views here.

class BuildingApiView(APIView):
    def get(self, request, building_id=None):
        if building_id is not None:
            building_obj=get_object_or_404(Building, id=building_id)
            serializer=BuildingSerializer(building_obj)
        else:
            bulding_obj=Building.objects.all()
            serializer=BuildingSerializer(building_obj, many=True)
        return success_response(serializer.data, message='success retrieved data')
    
    def post(self, request):
        serializer=BuildingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success create data')
        return error_400_response(serializer)

    def put(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        serializer=BuildingSerializer(building_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
        return error_400_response(serializer)
        
    def patch(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        serializer=BuildingSerializer(building_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="success update data")
        return error_400_response(serializer)

    def delete(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        building_obj.delete()
        return delete_reponse(message='success delete data')
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class RoomApiView(APIView):
    def get(self, request, room_id=None):
        if room_id is not None:
            room_obj=get_object_or_404(Room, id=room_id)
            serializer=RoomSerializer(room_obj)
        else:
            room_obj=Room.objects.all()
            serializer=RoomSerializer(room_obj, many=True)
        return success_response(serializer.data, message='success retrieved data')
    
    def post(self, request):
        serializer=RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success create data')
        return error_400_response(serializer)

    def put(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        serializer=RoomSerializer(room_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
        return error_400_response(serializer)
        
    def patch(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        serializer=RoomSerializer(room_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="success update data")
        return error_400_response(serializer)

    def delete(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        room_obj.delete()
        return delete_reponse(message='success delete data')
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class FacultyApiView(APIView):
    def get(self, request, faculty_id=None):
        if faculty_id is not None:
            faculty_obj=get_object_or_404(Faculty, id=faculty_id)
            serializer=FacultySerializer(faculty_obj)
        else:
            faculty_obj=Faculty.objects.all()
            serializer=FacultySerializer(faculty_obj, many=True)
        return success_response(serializer.data, message='success retrieved data')
    
    def post(self, request):
        serializer=FacultySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success create data')
        return error_400_response(serializer)

    def put(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
        return error_400_response(serializer)
        
    def patch(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        serializer=FacultySerializer(faculty_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="success update data")
        return error_400_response(serializer)

    def delete(self, request, faculty_id):
        faculty_obj=get_object_or_404(Faculty, id=faculty_id)
        faculty_obj.delete()
        return delete_reponse(message='success delete data')
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class DepartmentApiView(APIView):
    def get(self, request, department_id=None):
        if department_id is not None:
            department_obj=get_object_or_404(Department, id=department_id)
            serializer=DepartmentSerializer(department_obj)
        else:
            department_obj=Department.objects.all()
            serializer=DepartmentSerializer(department_obj, many=True)
        return success_response(serializer.data, message='success retrieved data')
    
    def post(self, request):
        serializer=DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success create data')
        return error_400_response(serializer)

    def put(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
        return error_400_response(serializer)
        
    def patch(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        serializer=DepartmentSerializer(department_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message="success update data")
        return error_400_response(serializer)

    def delete(self, request, department_id):
        department_obj=get_object_or_404(Department, id=department_id)
        department_obj.delete()
        return delete_reponse(message='success delete data')
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    