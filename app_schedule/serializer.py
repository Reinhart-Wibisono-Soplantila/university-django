from rest_framework import serializers
from .models import Schedule, RegisteredSchedule
from app_common.models import Term, Department
from app_course.models import Course
from app_building.models import Building, Room
from app_staff.models import TeachingStaff
from app_common.serializers import DepartmentSerializer
from app_course.serializers import CourseSerializer
from app_building.serializers import BuildingSerializer, RoomSerializer
from app_staff.serializers import TeachingStaffSerializer_Get
from django.db import transaction

class ScheduleSerializer(serializers.ModelSerializer):
    semester_pack_display = serializers.CharField(source='get_semester_pack_display', read_only=True)

    department=DepartmentSerializer(read_only=True)
    department_id=serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all(),
        write_only=True,
        required=True,
        source='department',
        error_messages={
            'does_not_exist': 'Department dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Department ID harus berupa angka',
            'required': 'Field Department harus diisi!'})
    
    course=CourseSerializer(read_only=True)
    course_id=serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        write_only=True,
        required=True,
        source='course',
        error_messages={
            'does_not_exist': 'Course dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Course ID harus berupa angka',
            'required': 'Field Course harus diisi!'})
    
    building=BuildingSerializer(read_only=True)
    building_id=serializers.PrimaryKeyRelatedField(
        queryset=Building.objects.all(),
        write_only=True,
        required=True,
        source='building',
        error_messages={
            'does_not_exist': 'Building dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Building ID harus berupa angka',
            'required': 'Field building_id harus diisi!'}
    )
    
    room=RoomSerializer(read_only=True)
    room_id=serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(),
        write_only=True,
        required=True,
        source='room',
        error_messages={
            'does_not_exist': 'Room dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Room ID harus berupa angka',
            'required': 'Field Room harus diisi!'})
    
    teaching_staff=TeachingStaffSerializer_Get(read_only=True)
    teaching_staff_id=serializers.PrimaryKeyRelatedField(
        queryset=TeachingStaff.objects.all(), 
        write_only=True,
        required=True,
        source='teaching_staff',
        error_messages={
            'does_not_exist': 'Teaching Staff dengan ID {pk_value} tidak ditemukan',
            'incorrect_type': 'Teaching Staff ID harus berupa angka',
            'required': 'Field Teaching Staff harus diisi!'})
    
    class Meta:
        model = Schedule
        fields = '__all__'  
        read_only_fields = ['remaining_quota', 'registered_quota']

    def validate(self, data):
        room = data.get('room')
        building = data.get('building')
        
        if room and building and room.building != building:
            raise serializers.ValidationError({
                'room_id': 'Ruangan tidak berada di gedung yang dipilih'
            })
        return data
    
    def validate_max_quota(self, value):
        instance = self.instance
        if instance and value < instance.registered_quota:
            raise serializers.ValidationError(
                f"Max quota ({value}) cannot be less than the number of registered students ({instance.registered_quota})."
            )
        return value
    
    def validate_remaining_quota(self, value):
        if 'remaining_quota' in value and value['remaining_quota'] <= 0:
            raise serializers.ValidationError({"remaining_quota": "Quota is full."})
        return value
    
    # coba buat seolah room bergantung dari building yang dipilih
    
    def update(self, instance, validated_data):
        max_quota=validated_data.get('max_quota', instance.max_quota)
        
        if max_quota < instance.registered_quota:
            raise serializers.ValidationError("Max quota cannot be less than the number of registered students.")

        if max_quota!=instance.max_quota:
            validated_data['remaining_quota']=max_quota-instance.registered_quota

        return super().update(instance, validated_data)
    

class RegisterScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model=RegisteredSchedule
        fields=['student', 'schedule']
        read_only_fields=['term']
    
    @transaction.atomic
    def create(self, validated_data):
        schedules = validated_data.get('schedule', [])
        student = validated_data.get('student')
        term = Term.objects.get(is_activate=1)
        
        schedules_to_lock=Schedule.objects.filter(id__in=[s.id for s in self.schedules]).select_for_update()
        locked_schedules={s.id: s for s in schedules_to_lock}
        
        for schedule in schedules:
            if locked_schedules[schedule.id].remaining_quota <= 0:
                raise serializers.ValidationError(f"Schedule {schedule.id} is full.")
        
        
        # Cek apakah sudah ada pendaftaran untuk siswa dan term ini
        existing_schedule = RegisteredSchedule.objects.filter(student=student, term=term).select_for_update().first()
        
        if existing_schedule:
            # Jika sudah ada, langsung lakukan update
            schedule_ids = [s.id for s in schedules]
            existing_schedule.update_schedule(schedule_ids)
            return existing_schedule

        validated_data['term'] = term
        
        # Simpan instance terlebih dahulu
        instance = super().create(validated_data)

        # Panggil update_schedule di model untuk penyesuaian kuota
        schedule_ids = [s.id for s in schedules]
        instance.update_schedule(schedule_ids)

        return instance



    # UPDATE DENGAN MEMASUKKAN UPDATE_SCHEDULE DARI MODELS
    # def update(self, instance, validated_data):
    #     new_schedules = validated_data.get('schedule', [])
    #     schedule_ids = [s.id for s in new_schedules]

    #     for schedule in new_schedules:
    #         if schedule.remaining_quota <= 0:
    #             raise serializers.ValidationError(f"Schedule {schedule.id} is full.")

    #     # Panggil logika kuota dan perubahan jadwal
    #     instance.update_schedule(schedule_ids)

    #     return instance

    
    # ORI
    # def create(self, validated_data):
    #     schedules = validated_data.get('schedule', [])
    #     for schedule in schedules:
    #         if schedule.remaining_quota <= 0:
    #             raise serializers.ValidationError(f"Schedule {schedule.id} is full.")
        
    #     term=Term.objects.get(is_activate=1)
    #     validated_data['term']=term
    #     return super().create(validated_data)
    
    # def update(self, instance, validated_data):
        
    #     new_schedules = validated_data.get('schedule', [])
    #     schedule_ids = [s.id for s in new_schedules]

    #     for schedule in new_schedules:
    #         if schedule.remaining_quota <= 0:
    #             raise serializers.ValidationError(f"Schedule {schedule.id} is full.")

    #     instance.update_schedule(schedule_ids)
    
    
    #     old_schedules=set(instance.schedule.all())
    #     new_schedules=set(validated_data.get('schedule'))
    #     if not old_schedules==new_schedules:
    #         to_add = new_schedules - old_schedules
    #         to_remove = old_schedules - new_schedules
    #         if to_add:
    #             instance.schedule.add(*to_add)
    #         if to_remove:
    #             instance.schedule.remove(*to_remove)
    #     return super().update(instance, validated_data)