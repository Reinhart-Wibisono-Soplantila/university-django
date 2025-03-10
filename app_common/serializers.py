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
    
    def create(self, validated_data):
        # Generate term_code otomatis
        validated_data['term_code'] = f"{validated_data['year_start']}{validated_data['semester']}"

        # Cek apakah term_code sudah ada
        if Term.objects.filter(term_code=validated_data['term_code']).exists():
            raise serializers.ValidationError({"term_code": "Term code already exists. Please use a different year or semester."})

        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.year_start = validated_data.get('year_start', instance.year_start)
        instance.year_end = validated_data.get('year_end', instance.year_end)
        instance.semester = validated_data.get('semester', instance.semester)

        # Perbarui term_code otomatis
        instance.term_code = f"{instance.year_start}{instance.semester}"

        # Cek apakah term_code yang baru sudah ada
        if Term.objects.exclude(id=instance.id).filter(term_code=instance.term_code).exists():
            raise serializers.ValidationError({"term_code": "Term code already exists. Please use a different year or semester."})

        instance.save()
        return instance

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields='__all__'