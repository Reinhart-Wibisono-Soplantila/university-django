from rest_framework import serializers
from .models import Schedule, RegisteredSchedule
from app_common.models import Term

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
    
    def create(self, validated_data):
        term=Term.objects.get(is_activate=1).term_code
        validated_data['term']=term
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        old_schedules=set(instance.schedule.all())
        new_schedules=set(validated_data.get('schedule'))
        if not old_schedules==new_schedules:
            to_add = new_schedules - old_schedules
            to_remove = old_schedules - new_schedules
            if to_add:
                instance.schedule.add(*to_add)
            if to_remove:
                instance.schedule.remove(*to_remove)
        return super().update(instance, validated_data)