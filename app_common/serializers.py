from rest_framework import serializers
from .models import Term, Grade, Status, Faculty, Department, EducationLevel, AcademicProgram
from django.shortcuts import get_object_or_404
from django.db import transaction

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
        
        if year_start is not None and semester is not None:
            term_code=f"{year_start}{semester}"            
            if Term.objects.filter(term_code=term_code).exists():
                raise serializers.ValidationError({"year_start": "Year or semester already exist. Please use a different year or semester."})
            
            data["term_code"] = term_code
        return data
    
    def validate_is_active(self, value):
        any_active_term=Term.objects.filter(is_active=1).count()
        if any_active_term>=1 and value==1:
            raise serializers.ValidationError("There is only one active term.")
        if any_active_term==0 and value==0:
            raise serializers.ValidationError("There must be one active term.")
        return value
    
    def create(self, validated_data):
        year_start = validated_data.get('year_start')
        semester = validated_data.get('semester')
        validated_data['year_end']=year_start+1
        validated_data['term_code'] = f"{year_start}{semester}"
        
        if validated_data.get('is_active'):
            Term.objects.filter(is_active=1).update(is_active=False)
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        year_start = validated_data.get('year_start', instance.year_start)
        semester = validated_data.get('semester', instance.semester)
        new_term_code = f"{year_start}{semester}"
        
        if Term.objects.exclude(id=instance.id).filter(term_code=new_term_code).exists():
            raise serializers.ValidationError({"term_code": "Year or semester already exists. Please use a different year or semester."})

        is_active=validated_data.get("is_active", instance.is_active)
        if is_active!=instance.is_active:
            if is_active:
                Term.objects.exclude(id=instance.id).update(is_active=0)
            else:
                if not Term.objects.exclude(id=instance.id).filter(is_active=1).exists():
                    raise serializers.ValidationError("There must be one active term.")
            
        validated_data["term_code"] = new_term_code
        validated_data["year_end"] = year_start + 1
        return super().update(instance, validated_data)

class StatusSerializers(serializers.ModelSerializer):
    class Meta:
        model=Status
        fields='__all__'

class EducationLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model=EducationLevel
        fields='__all__'

class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model=Faculty
        fields='__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    faculty_id=serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        write_only=True,
        required=True,
        source='faculty',
        error_messages={
            'does_not_exist': 'Faculty dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Faculty ID harus berupa angka',
            'required': 'Field Faculty harus diisi!'}
    )
    faculty= FacultySerializer(read_only=True)
    
    class Meta:
        model=Department
        fields='__all__'
    
    def _generate_department_code(self, faculty):
        faculty_code=faculty.faculty_code
        last_department=Department.objects.filter(faculty=faculty).order_by('-department_code').first()
        if last_department is not None:
            last_number=int(last_department.department_code[1:])
            new_number=last_number+1
        else:
            new_number=1
        department_code=f"{faculty_code}{new_number:03d}"
        return department_code
    
    def create(self, validated_data):
        faculty=validated_data['faculty']
        validated_data['department_code']=self._generate_department_code(faculty)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'faculty' in validated_data and instance.faculty != validated_data['faculty']:
            faculty=validated_data['faculty']
            validated_data['department_code']=self._generate_department_code(faculty)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'faculty' in rep and rep['faculty'] is not None:
            data=rep['faculty']
            data.pop('created_at', None)
            data.pop('updated_at', None)
        return rep

class AcademicProgramSerializer(serializers.ModelSerializer):
    faculty_id=serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all(),
        write_only=True,
        required=True,
        source='faculty',
        error_messages={
            'does_not_exist': 'Faculty dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Faculty ID harus berupa angka',
            'required': 'Field Faculty harus diisi!'}
    )
    faculty=FacultySerializer(read_only=True)
    
    education_level_id=serializers.PrimaryKeyRelatedField(
        queryset=EducationLevel.objects.all(),
        write_only=True,
        required=True, 
        source='education_level',
        error_messages={
            'does_not_exist': 'Education Level dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Education Level ID harus berupa angka',
            'required': 'Field Education Level harus diisi!'}
    )
    education_level=EducationLevelSerializer(read_only=True)
    
    class Meta:
        model=AcademicProgram
        fields='__all__'
    
    def _generate_program_code(self, faculty, education_level):
        faculty_code = faculty.faculty_code
        last_program=AcademicProgram.objects.filter(faculty=faculty, education_level=education_level).order_by('-academic_program_code').first()
        new_number = int(last_program.academic_program_code[-3:])+1 if last_program else 1
        level_abr=education_level.abbreviation
        education_level_code=level_abr[1]
        return f"{faculty_code}1{education_level_code:02d}1{new_number:03d}"
    
    def create(self, validated_data):
        faculty=validated_data['faculty']
        education_level=validated_data["education_level"]
        validated_data['academic_program_code']=self._generate_program_code(faculty, education_level)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        faculty_changed= 'faculty' in validated_data and validated_data['faculty'] != instance.faculty
        education_level_changed= 'education_level' in validated_data and validated_data['education_level'] != instance.education_level
        if faculty_changed or education_level_changed:
            faculty=validated_data.get('faculty', instance.faculty)
            education_level=validated_data.get('education_level', instance.education_level)
            validated_data['academic_program_code']=self._generate_program_code(faculty, education_level)
        return super().update(instance, validated_data)
    
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if "faculty" in rep and rep['faculty'] is not None:
            data=rep["faculty"]
            data.pop("created_at", None)
            data.pop("updated_at", None)
        if "education_level" in rep and rep["education_level"] is not None:
            data=rep["education_level"]
            data.pop("created_at", None)
            data.pop("updated_at", None)
        return rep