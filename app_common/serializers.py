from rest_framework import serializers
from .models import Term, Grade, Status

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grade
        fields='__all__'
        
class TermSerializers(serializers.ModelSerializer):
    class Meta:
        model=Term
        fields='__all__'

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields='__all__'