from rest_framework import serializers
from .models import Student, StudentProfile
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework.exceptions import ValidationError

# class StudentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Student
#         fields='__all__'
#         read_only_fields=['nim']
    
#     def validate(self, data):
#         faculty = data.get("faculty") or self.instance.faculty
#         department = data.get("department") or self.instance.department
#         if "faculty" in data and department and not faculty.departments.filter(id=department.id).exists():
#             raise ValidationError({"detail": "Department is not listed in this Faculty"})
#         return data
    
#     def update(self, instance, validated_data):
#         faculty=validated_data.get('faculty', instance.faculty)
#         department=validated_data.get('department', instance.department)
#         registration_year=validated_data.get('registration_year', instance.registration_year)
        
#         faculty_code=faculty.faculty_code if faculty!=instance.faculty else instance.faculty.faculty_code
#         department_code=department.id if department!=instance.department else instance.department.id
#         year=str(registration_year)[-2:] if registration_year!=instance.registration_year else str(instance.registration_year)[-2:]
        
#         if faculty_code!=instance.faculty.faculty_code or registration_year!=instance.registration_year or department_code!=instance.department.id:
#             last_student=Student.objects.filter(faculty=faculty, registration_year=registration_year, department=department).order_by('-nim').first()
#             student_number=int(last_student.nim[-3:])+1 if last_student else 1
#             instance.nim=f'{faculty_code}{department_code:02d}1{year}1{student_number:03d}'
                
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
        
#         instance.save()
#         return instance
    
class StudentProfileSerializer(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=StudentProfile
        fields='__all__'
        read_only_fields = ['student']
        
class StudentSerializer(serializers.ModelSerializer):
    profile = StudentProfileSerializer(write_only=True, required=False)  # Tambahkan profile

    class Meta:
        model = Student
        fields = '__all__'
        read_only_fields = ['nim']
    
    # perbaiki nama validate
    def validate(self, data):
        faculty = data.get("faculty") or self.instance.faculty
        department = data.get("department") or self.instance.department
        if "faculty" in data and department and not faculty.departments.filter(id=department.id).exists():
            raise ValidationError({"detail": "Department is not listed in this Faculty"})
        return data

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)  # Ambil data profile jika ada
        student = Student.objects.create(**validated_data)
        if profile_data:
            StudentProfile.objects.create(student=student, **profile_data)  # Buat profile

        return student

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)

        # Update data student
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update atau buat data profile
        if profile_data:
            profile, created = StudentProfile.objects.get_or_create(student=instance)
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance