from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Grade, Term, Status
from .serializers import GradeSerializer, TermSerializers, StatusSerializers

# Create your views here.
class GradeApiView(APIView):
    def get(self, request, grade_id=None):
        grade_obj=Grade.objects.filter(id=grade_id)
        serializer=GradeSerializer(grade_obj, many=True)
        return Response({
            "status_code":status.HTTP_200_OK,
            "status":"success",
            "message":"success retrieved data",
            "data":serializer.data
        }, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer=GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status_code":status.HTTP_200_OK,
                "status":"success",
                "message":"success insert data",
                "data":serializer.data
            }, status=status.HTTP_200_OK)

    def put(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status_code":status.HTTP_200_OK,
                "status":"success",
                "message":"success update data",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
    
    def patch(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status_code":status.HTTP_200_OK,
                "status":"success",
                "message":"success update data",
                "data":serializer.data
            }, status=status.HTTP_200_OK)
    
    def delete(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        grade_obj.delete()
        return Response({
            "status_code":status.HTTP_200_OK,
            "status":"success",
            "message":"success delete data",
        }, status=status.HTTP_200_OK)
        
        