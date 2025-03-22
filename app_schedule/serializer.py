from rest_framework import serializers
from .models import Schedule

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