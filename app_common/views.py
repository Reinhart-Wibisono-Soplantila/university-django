from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Grade, Term, Status
from .serializers import GradeSerializer, TermSerializers, StatusSerializers
from .response import success_response, delete_reponse, options_response

# Create your views here.
class GradeApiView(APIView):
    def get(self, request, grade_id=None):
        grade_obj=Grade.objects.filter(id=grade_id)
        serializer=GradeSerializer(grade_obj, many=True)
        return success_response(serializer.data, message='success retrieved data')
        
    def post(self, request):
        serializer=GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success insert data')
            # return Response({
            #     "status_code":status.HTTP_200_OK,
            #     "status":"success",
            #     "message":"success insert data",
            #     "data":serializer.data
            # }, status=status.HTTP_200_OK)

    def put(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
            # return Response({
            #     "status_code":status.HTTP_200_OK,
            #     "status":"success",
            #     "message":"success update data",
            #     "data":serializer.data
            # }, status=status.HTTP_200_OK)
    
    def patch(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        serializer=GradeSerializer(grade_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
            # return Response({
            #     "status_code":status.HTTP_200_OK,
            #     "status":"success",
            #     "message":"success update data",
            #     "data":serializer.data
            # }, status=status.HTTP_200_OK)
    
    def delete(self, request, grade_id):
        grade_obj=get_object_or_404(Grade, id=grade_id)
        grade_obj.delete()
        return delete_reponse(message='success delete data')
        # return Response({
        #     "status_code":status.HTTP_200_OK,
        #     "status":"success",
        #     "message":"success delete data",
        # }, status=status.HTTP_200_OK)

    def options(self, request, *args, **kwargs):
        return options_response()
    
class TermApiView(APIView):
    def get(self, request, term_id):
        term_obj=Term.objects.filter(id=term_id)
        serializer=TermSerializers(term_obj, many=True)
        return success_response(serializer.data, message='success retrieved data')
    
    def post(self, request):
        serializer=TermSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success insert data')
        
    def put(self, request, term_id):
        term_obj=get_object_or_404(Term, id=term_id)
        serializer=TermSerializers(term_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success update data')
    
    def patch(self, request, term_id):
        term_obj=get_object_or_404(Term, id=term_id)
        serializer=TermSerializers(term_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return success_response(serializer.data, message='success insert data')
        
    def delete(self, request, term_id):
        term_obj=get_object_or_404(Term, id=term_id)
        term_obj.delete()
        return delete_reponse(message='success delete data')
    
    def options(self, request, *args, **kwargs):
        return options_response()