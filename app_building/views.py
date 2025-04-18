from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .models import Building, Room
from .serializers import BuildingSerializer, RoomSerializer

# Create your views here.
class BuildingApiView(APIView):
    def get(self, request, building_id=None):
        if building_id is not None:
            building_obj=get_object_or_404(Building, id=building_id)
            serializers=BuildingSerializer(building_obj)
        else:
            building_obj=Building.objects.all()
            serializers=BuildingSerializer(building_obj, many=True)
        return success_response(serializers.data, message='success retrieve data')
    
    def post(self, request):
        serializers=BuildingSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
            return success_response(serializers.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def put(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        serializers=BuildingSerializer(building_obj, data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
            return success_response(serializers.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        serializers=BuildingSerializer(building_obj, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
            return success_response(serializers.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def delete(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        building_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class RoomApiView(APIView):
    def get(self, request, room_id=None):
        if room_id is not None:
            room_obj=get_object_or_404(Room, id=room_id)
            serializers=RoomSerializer(room_obj)
        else:
            room_obj=Room.objects.all()
            serializers=RoomSerializer(room_obj, many=True)
        return success_response(serializers.data, message='success retrieve data')
    
    def post(self, request):
        serializers=RoomSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
            return success_response(serializers.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def put(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        serializers=RoomSerializer(room_obj, data=request.data)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
            return success_response(serializers.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        serializers=RoomSerializer(room_obj, data=request.data, partial=True)
        serializers.is_valid(raise_exception=True)
        try:
            serializers.save()
            return success_response(serializers.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def delete(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        room_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
 