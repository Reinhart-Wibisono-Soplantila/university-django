from rest_framework import serializers
from .models import Term, Grade, Status, Faculty, Department, EducationLevel, AcademicProgram

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
            
        instance.term_code = new_term_code
        instance.year_start = year_start
        instance.year_end = year_start + 1
        instance.semester = semester
        instance.is_active = is_active
        instance.save()
        return instance

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

    def update(self, instance, validated_data):
        faculty=validated_data['faculty']
        if faculty!=instance.faculty:
            faculty_code=faculty.faculty_code
            last_department=Department.objects.filter(faculty=faculty).order_by('-department_code').first()
            if last_department is not None:
                las_number=int(last_department.department_code[1:])
                new_number=las_number+1
            else:
                new_number=1
            department_code=f"{faculty_code}{new_number:03d}"
            validated_data['department_code']=department_code
        return super().update(instance, validated_data)

class AcademicProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model=AcademicProgram
        fields='__all__'
    
    def create(self, validated_data):
        faculty=validated_data['faculty']
        faculty_code=faculty.faculty_code
        # department=validated_data['department']
        # department_code=department.department_code
        education_level=validated_data['education_level']
        last_program=AcademicProgram.objects.filter(faculty=faculty, education_level=education_level).order_by('-academic_program_code').first()
        if last_program is not None:
            las_number=int(last_program.academic_program_code[-3:])
            new_number=las_number+1
        else:
            new_number=1
        education_level=education_level.abbreviation
        if education_level=='S1':
            education_level_code=1
        elif education_level=='S2':
            education_level_code=2
        elif education_level=='S3':
            education_level_code=3
        elif education_level=='S4':
            education_level_code=4
        academic_program_code=f"{faculty_code}1{education_level_code:02d}1{new_number:03d}"
        validated_data['academic_program_code']=academic_program_code
        return super().create(validated_data)

    def update(self, instance, validated_data):
        faculty = validated_data.get('faculty', instance.faculty)
        education_level = validated_data.get('education_level', instance.education_level)
        if faculty!=instance.faculty  or education_level!=instance.education_level:
            last_program=AcademicProgram.objects.filter(faculty=faculty, education_level=education_level).order_by('-academic_program_code').first()
            if last_program is not None:
                las_number=int(last_program.academic_program_code[-3:])
                new_number=las_number+1
            else:
                new_number=1
            
            faculty_code=faculty.faculty_code
            education_level=education_level.abbreviation
            if education_level=='S1':
                education_level_code=1
            elif education_level=='S2':
                education_level_code=2
            elif education_level=='S3':
                education_level_code=3
            academic_program_code=f"{faculty_code}1{education_level_code:02d}1{new_number:03d}"
            validated_data['academic_program_code']=academic_program_code
        return super().update(instance, validated_data)