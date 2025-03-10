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
    
    def validate(self, data):
        year_start=data.get("year_start")
        year_end=data.get("year_end")
        
        if year_end is not None and year_start is not None:
            if year_start >= year_end:
                raise serializers.ValidationError({"year_end": "Year end must be greater than year start."})
        return data

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields='__all__'