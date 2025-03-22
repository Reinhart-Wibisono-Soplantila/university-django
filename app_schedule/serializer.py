from rest_framework import serializers
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    semester_pack_display = serializers.CharField(source='get_semester_pack_display', read_only=True)

    class Meta:
        model = Schedule
        fields = '__all__'  
        read_only_fields = ['remaining_quota', 'registered_quota']

    def validate(self, data):
        if 'remaining_quota' in data and data['remaining_quota'] < 0:
            raise serializers.ValidationError({"remaining_quota": "Remaining quota tidak boleh negatif."})
        return data