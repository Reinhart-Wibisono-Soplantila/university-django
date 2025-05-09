from rest_framework import serializers
from .models import Term, Grade, Status, Faculty, Department, EducationLevel, AcademicProgram
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
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
    faculty_id=serializers.IntegerField(
        write_only=True,
        required=True,
        allow_null=False,
    )
    faculty= FacultySerializer(read_only=True)
    
    class Meta:
        model=Department
        fields='__all__'
    
    def validate_faculty_id(self, value):
        if not Faculty.objects.filter(id=value).exists():
            raise serializers.ValidationError({"faculty: Faculty does not exist"})
        return value
    
    def _generate_department_code(self, faculty_id):
        faculty = Faculty.objects.get(id=faculty_id)
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
        validated_data['department_code']=self._generate_department_code(validated_data['faculty_id'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        faculty_id=validated_data.get('faculty_id', instance.faculty_id)
        if faculty_id!=instance.faculty_id:
            validated_data['department_code']=self._generate_department_code(faculty_id)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        rep=super().to_representation(instance)
        if 'faculty' in rep and rep['faculty'] is not None:
            data=rep['faculty']
            data.pop('created_at', None)
            data.pop('updated_at', None)
        return rep

class AcademicProgramSerializer(serializers.ModelSerializer):
    faculty_id=serializers.IntegerField(
        required=True,
        write_only=True,
        allow_null=False
    )
    faculty=FacultySerializer(read_only=True)
    
    education_level_id=serializers.IntegerField(
        required=True,
        write_only=True,
        allow_null=False
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
        level_code={'S1':1, 'S2':2, 'S3':3, 'S4':4}
        education_level_code=level_code.get(level_abr, 0)
        return f"{faculty_code}1{education_level_code:02d}1{new_number:03d}"
    
    def create(self, validated_data):
        faculty_id=validated_data["faculty_id"]
        faculty=Faculty.objects.get(id=faculty_id)
        education_level=validated_data['education_level']
        
        validated_data['academic_program_code']=self.generate_program_code(faculty, education_level)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        faculty_id=validated_data.get('faculty_id', instance.faculty_id)
        faculty=Faculty.objects.get(id=faculty_id)
        education_level = validated_data.get('education_level', instance.education_level)
        
        if faculty!=instance.faculty  or education_level!=instance.education_level:
            self._generate_program_code(faculty, education_level)
            
            academic_program_code=self._generate_program_code(faculty, education_level)
            validated_data['academic_program_code']=academic_program_code
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
            