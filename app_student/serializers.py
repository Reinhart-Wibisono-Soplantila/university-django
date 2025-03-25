from rest_framework import serializers
from .models import Student
from phonenumber_field.serializerfields import PhoneNumberField

class StudentSerializer(serializers.ModelSerializer):
    phone_number=PhoneNumberField()
    class Meta:
        model=Student
        fields='__all__'
        read_only_fields=['nim']
    
    def update(self, instance, validated_data):
        faculty=validated_data.get('faculty', instance.faculty)
        department=validated_data.get('department', instance.department)
        registration_year=validated_data.get('registration_year', instance.registration_year)
        
        faculty_code=faculty.faculty_code if faculty!=instance.faculty else instance.faculty.faculty_code
        department_code=department.id if department!=instance.department else instance.department.id
        year=str(registration_year)[-2:] if registration_year!=instance.registration_year else str(instance.registration_year)[-2:]
        
        if registration_year!=instance.registration_year or department!=instance.department:
            last_student=Student.objects.filter(registration_year=registration_year, department=department).order_by('-nim').first()
            student_number=int(last_student.nim[-3:])+1 if last_student else 1
            instance.nim=f'{faculty_code}{department_code:02d}1{year}1{student_number:03d}'
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance