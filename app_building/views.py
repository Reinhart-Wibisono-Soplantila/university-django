from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import success_response, created_response, options_response, delete_reponse, error_400_response
from .models import Building, Room
from .serializers import BuildingSerializer, RoomSerializer

# Create your views here.
class BuildingApiView(APIView):
    def get(self, request, building_id=None):
        if building_id is not None:
            building_obj=get_object_or_404(Building, id=building_id)
            serializer=BuildingSerializer(building_obj)
        else:
            building_obj=Building.objects.all()
            serializer=BuildingSerializer(building_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
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
        return success_response(serializer.data, message='success retrieve data')
    
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
 