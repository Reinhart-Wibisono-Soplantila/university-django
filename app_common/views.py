from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Grade, Term, Status
from .serializers import GradeSerializer, TermSerializers, StatusSerializers

# Create your views here.

        