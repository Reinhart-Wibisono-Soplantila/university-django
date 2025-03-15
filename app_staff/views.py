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
            serializer-PositionTeachingSerializer(position_obj, many=True)
        return success_response(serializer)