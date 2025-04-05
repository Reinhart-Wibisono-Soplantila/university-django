from rest_framework import serializers
from .models import Term, Grade, Status, Faculty, Department

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Grade
        fields='__all__'
        
class TermSerializers(serializers.ModelSerializer):
    class Meta:
        model=Term
        fields='__all__'
        read_only_fields=['term_code', 'year_end']
    
    def validate(self, data):
        year_start=data.get("year_start")
        semester = data.get("semester")
        
        if year_start is not None:
            data['year_end']=year_start+1
            term_code=f"{year_start}{semester}"            
            if Term.objects.filter(term_code=term_code).exists():
                raise serializers.ValidationError({"year_start": "Year or semester already exist. Please use a different year or semester."})
            
            data["term_code"] = term_code
        return data
    
    def validate_is_active(self, value):
        any_active_term=Term.objects.filter(is_active=1).count()
        if any_active_term>1 and value==1:
            raise serializers.ValidationError("There is only one active term.")
        if any_active_term==0 and value==0:
            raise serializers.ValidationError("There must be one active term.")
        return value
    
    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        year_start = validated_data.get('year_start', instance.year_start)
        # year_end = validated_data.get('year_end', instance.year_end)
        semester = validated_data.get('semester', instance.semester)
        
        if Term.objects.exclude(id=instance.id).filter(term_code=instance.term_code).exists():
            raise serializers.ValidationError({"term_code": "Term code already exists. Please use a different year or semester."})

        is_active=validated_data.get("is_active")
        if is_active!=instance.is_active:
            if is_active==1:
                Term.objects.exclude(id=instance.id).update(is_active=0)
            elif is_active==0:
                if not Term.objects.filter(is_active=1).exists():
                    raise serializers.ValidationError("There must be one active term.")
            
        instance.year_start = year_start
        instance.year_end = year_start + 1
        instance.semester = semester
        instance.term_code = f"{year_start}{semester}"
        instance.is_active = is_active
        instance.save()
        return instance

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields='__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model=Faculty
        fields='__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'
    
    def create(self, validated_data):
        faculty=validated_data['faculty']
        faculty_code=faculty.faculty_code
        last_department=Department.objects.filter(faculty=faculty).order_by('-department_code').first()
        if last_department is not None:
            las_number=int(last_department.department_code[1:])
            new_number=las_number+1
        else:
            new_number=1
        department_code=f"{faculty_code}{new_number:03d}"
        validated_data['department_code']=department_code
        return super().create(validated_data)