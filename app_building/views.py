from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .models import Building, Room
from .serializers import *
from django.core.cache import cache
from django.db import transaction
from django.conf import settings
from university.permissions import isAdmin
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class BuildingApiView(APIView):
    CACHE_TIMEOUT =getattr(settings, 'CACHE_TIMEOUT', 60*60)
    permission_classes=[IsAuthenticated, isAdmin]
    
    @staticmethod
    def clear_cache_building(building_id=None):
        keys=["building_all"]
        if building_id:
            keys.append(f"building_{building_id}")
        cache.delete_many(keys)
    
    def get_queryset(self):
        return Building.objects.select_related("faculty")
    
    def get(self, request, building_id=None):
        cache_key=f"building_{building_id}" if building_id else "building_all"
        data = cache.get(cache_key)
        if not data:
            if building_id is not None:
                building_obj=get_object_or_404(self.get_queryset(), id=building_id)
                serializer=BuildingSerializer(building_obj)
            else:
                building_obj=self.get_queryset().all()
                serializer=BuildingSerializer(building_obj, many=True)
            data = serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=BuildingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                BuildingApiView.clear_cache_building()
                return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def put(self, request, building_id):
        building_obj=get_object_or_404(self.get_queryset(), id=building_id)
        serializer=BuildingSerializer(building_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                BuildingApiView.clear_cache_building(building_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def patch(self, request, building_id):
        building_obj=get_object_or_404(self.get_queryset(), id=building_id)
        serializer=BuildingSerializer(building_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                BuildingApiView.clear_cache_building(building_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def delete(self, request, building_id):
        building_obj=get_object_or_404(self.get_queryset(), id=building_id)
        try:
            with transaction.atomic():
                building_obj.delete()
                BuildingApiView.clear_cache_building(building_id)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
    
class RoomApiView(APIView):
    CACHE_TIMEOUT = getattr(settings, 'CACHE_TIMEOUT', 60*60)
    
    permission_classes=[IsAuthenticated, isAdmin]
    
    @staticmethod
    def clear_cache_room(room_id=None):
        keys=["room_all"]
        if room_id:
            keys.append(f"room_{room_id}")
        cache.delete_many(keys)
    
    def get_queryset(self):
        return Room.objects.select_related("building")
    
    def get(self, request, room_id=None):
        cache_key=f"room_{room_id}" if room_id else "room_all"
        data=cache.get(cache_key)
        if not data:
            if room_id is not None:
                room_obj=get_object_or_404(self.get_queryset(), id=room_id)
                serializer=RoomSerializer(room_obj)
            else:
                room_obj=self.get_queryset().all()
                serializer=RoomSerializer(room_obj, many=True)
            data=serializer.data
            cache.set(cache_key, data, timeout=self.CACHE_TIMEOUT)
        return success_response(data, message='success retrieve data')
    
    def post(self, request):
        serializer=RoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                RoomApiView.clear_cache_room()
                return success_response(serializer.data, message='success create data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def put(self, request, room_id):
        room_obj=get_object_or_404(self.get_queryset(), id=room_id)
        serializer=RoomSerializer(room_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                RoomApiView.clear_cache_room(room_id)
                return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def patch(self, request, room_id):
        room_obj=get_object_or_404(self.get_queryset(), id=room_id)
        serializer=RoomSerializer(room_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            with transaction.atomic():
                serializer.save()
                RoomApiView.clear_cache_room(room_id)
                return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            
    def delete(self, request, room_id):
        room_obj=get_object_or_404(self.get_queryset(), id=room_id)
        try:
            with transaction.atomic():
                room_obj.delete()
                RoomApiView.clear_cache_room(room_id)
                return delete_response()
        except IntegrityError as e:
            error_clean = str(e).replace('\n', ' ').replace('"', '')
            raise ValidationError({error_clean})
            # raise ValidationError({"detail": "Data grade sudah ada atau melanggar constraint."})
            