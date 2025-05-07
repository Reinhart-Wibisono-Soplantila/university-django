from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .models import Building, Room
from .serializers import *
from django.core.cache import cache

# Create your views here.
class BuildingApiView(APIView):
    CACHE_TIMEOUT = 60*60
    
    def get_queryset(self):
        return Building.objects.select_related("faculty")
    
    def get(self, request, building_id=None):
        if building_id is not None:
            cache_key=f"building_{building_id}"
            data = cache.get(cache_key)
            if not data:
                building_obj=get_object_or_404(self.get_queryset(), id=building_id)
                serializer=BuildingSerializer(building_obj)
                data = serializer.data
                cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        else:
            cache_key="building_all"
            data = cache.get(cache_key)
            if not data:
                building_obj=self.get_queryset().all()
                serializer=BuildingSerializer(building_obj, many=True)
                data = serializer.data
                cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=BuildingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            cache.delete("building_all")
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def put(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        serializer=BuildingSerializer(building_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            cache.delete(f"building_{building_id}")
            cache.delete("building_all")
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        serializer=BuildingSerializer(building_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            cache.delete(f"building_{building_id}")  # Invalidate cache detail
            cache.delete("building_all")
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def delete(self, request, building_id):
        building_obj=get_object_or_404(Building, id=building_id)
        try:
            building_obj.delete()
            cache.delete(f"building_{building_id}")  # Invalidate cache detail
            cache.delete("building_all")
            return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class RoomApiView(APIView):
    CACHE_TIMEOUT = 60*60
    
    def get_queryset(self):
        return Room.objects.select_related("building")
    
    def get(self, request, room_id=None):
        if room_id is not None:
            cache_key=f"room_{room_id}"
            data=cache.get(cache_key)
            if not data:
                room_obj=get_object_or_404(self.get_queryset(), id=room_id)
                serializer=RoomSerializer(room_obj)
                data=serializer.data
                cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        else:
            cache_key=f"room_all"
            data=cache.get(cache_key)
            if not data:
                room_obj=self.get_queryset().all()
                serializer=RoomSerializer(room_obj, many=True)
                data=serializer.data
                cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            cache.delete("room_all")
            return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def put(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        serializer=RoomSerializer(room_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            cache.delete("room_all")
            cache.delete(f"room_{room_id}")
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
        
    def patch(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        serializer=RoomSerializer(room_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            cache.delete("room_all")
            cache.delete(f"room_{room_id}")
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})

    def delete(self, request, room_id):
        room_obj=get_object_or_404(Room, id=room_id)
        try:
            room_obj.delete()
            cache.delete("room_all")
            cache.delete(f"room_{room_id}")
            return delete_reponse()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
 