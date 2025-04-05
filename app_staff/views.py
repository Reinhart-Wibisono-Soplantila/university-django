from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from university.response import *
from .serializers import *
from .models import *

# Create your views here.
class TeachingPositionApiView(APIView):
    def get(self, request, position_id=None):
        if position_id is not None:
            position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
            serializer=PositionTeachingSerializer(position_obj)
        else:
            position_obj=PositionTeachingStaff.objects.all()
            serializer=PositionTeachingSerializer(position_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')
    
    def post(self, request):
        serializer=PositionTeachingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        try:
            serializer.save()
            return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
        
    def put(self, request, position_id):
        position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
        serializer=PositionTeachingSerializer(position_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message='success update data')
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
        
    # def patch(self, request, position_id):
    #     position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
    #     serializer=PositionTeachingSerializer(position_obj, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     try:
    #         serializer.save()
    #         return success_response(serializer.data, message='success update data')
    #     except IntegrityError as e:
    #         raise serializer.ValidationError({"Integrity error": str(e)})
    
    def delete(self, request, position_id):
        position_obj=get_object_or_404(PositionTeachingStaff, id=position_id)
        position_obj.delete()
        return delete_reponse()
    
    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
        
class TeachingStaffApiView(APIView):
    def get(self, request, nip=None):
        if nip is not None:
            teaching_obj=get_object_or_404(TeachingStaff, nip=nip)
            serializer=TeachingStaffSerializer(teaching_obj)
        else:
            teaching_obj=TeachingStaff.objects.all()
            serializer=TeachingStaffSerializer(teaching_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')

    def post(self, request):
        serializer=TeachingStaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
    
    def put(self, request, nip):
        teaching_obj=get_object_or_404(TeachingStaff, nip=nip)
        serializer=TeachingStaffSerializer(teaching_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
        
    def patch(self, request, nip):
        teaching_obj=get_object_or_404(TeachingStaff, nip=nip)
        serializer=TeachingStaffSerializer(teaching_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
    
    def delete(self, request, nip):
        teaching_obj=get_object_or_404(TeachingStaff, nip=nip)
        # teaching_obj.areas_of_expertise.clear()
        teaching_obj.delete()
        return delete_reponse()

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
    
class AdministrativeStaffApiView(APIView):
    def get(self, request, nip=None):
        if nip is not None:
            administrative_obj=get_object_or_404(AdministrativeStaff, nip=nip)
            serializer=AdminStaffSerializer(administrative_obj)
        else:
            administrative_obj=AdministrativeStaff.objects.all()
            serializer=AdminStaffSerializer(administrative_obj, many=True)
        return success_response(serializer.data, message='success retrieve data')

    def post(self, request):
        serializer=AdminStaffSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success create data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
    
    def put(self, request, nip):
        administrative_obj=get_object_or_404(AdministrativeStaff, nip=nip)
        serializer=AdminStaffSerializer(administrative_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
        
    def patch(self, request, nip):
        administrative_obj=get_object_or_404(AdministrativeStaff, nip=nip)
        serializer=AdminStaffSerializer(administrative_obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return success_response(serializer.data, message="success update data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
    
    def delete(self, request, nip):
        administrative_obj=get_object_or_404(AdministrativeStaff, nip=nip)
        administrative_obj.delete()
        return delete_reponse()

    def options(self, request, *args, **kwargs):
        return super().options(request, *args, **kwargs)
            
class ExpertiseApiView(APIView):
    def get(self, request, expertise_id=None):
        if expertise_id is not None:
            expertise_obj=get_object_or_404(AreaOfExpertise, id=expertise_id)
            serializer=ExpertiseSerializer(expertise_obj)
        else:
            expertise_obj=AreaOfExpertise.objects.all()
            serializer=ExpertiseSerializer(expertise_obj, many=True)
        return success_response(serializer.data, message="success retrieve data")
    
    def post(self, request):
        serializer=ExpertiseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return created_response(serializer.data, message='success created data')
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
    
    def put(self, request, expertise_id):
        expertise_obj=get_object_or_404(AreaOfExpertise, id=expertise_id)
        serializer=ExpertiseSerializer(expertise_obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
            return created_response(serializer.data, message="success created data")
        except IntegrityError as e:
            raise serializer.ValidationError({"Integrity error": str(e)})
    
    def delete(self, request, expertise_id):
        expertise_obj=get_object_or_404(AreaOfExpertise, id=expertise_id)
        expertise_obj.delete()
        return delete_reponse()
            