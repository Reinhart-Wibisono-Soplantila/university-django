from rest_framework import serializers
from .models import Schedule, RegisteredSchedule
from app_common.models import Term
from django.db import transaction

class ScheduleSerializer(serializers.ModelSerializer):
    semester_pack_display = serializers.CharField(source='get_semester_pack_display', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'  
        read_only_fields = ['remaining_quota', 'registered_quota']

    def validate(self, data):
        if 'remaining_quota' in data and data['remaining_quota'] <= 0:
            raise serializers.ValidationError({"remaining_quota": "Quota is full."})
        return data
    
    def validate_max_quota(self, value):
        instance = self.instance
        if instance and value < instance.registered_quota:
            raise serializers.ValidationError(
                f"Max quota ({value}) cannot be less than the number of registered students ({instance.registered_quota})."
            )
        return value
    
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