from django.db import models, transaction
from django.db.models import F
from app_course.models import Course
from app_building.models import Building, Room
from app_staff.models import TeachingStaff
# Create your models here.
class Schedule(models.Model):
    semester_choices=[
        (1, "Semester 1"),
        (2, "Semester 2"),
        (3, "Semester 3"),
        (4, "Semester 4"),
        (5, "Semester 5"),
        (6, "Semester 6"),
        (7, "Semester 7"),
        (8, "Semester 8"),
    ]
    semester_pack=models.IntegerField(choices=semester_choices)
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='schedules')
    building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name='schedules')
    room=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='schedules')
    teaching_staff=models.ForeignKey(TeachingStaff, on_delete=models.CASCADE, related_name='schedules')
    max_quota=models.IntegerField()
    remaining_quota=models.IntegerField()
    registered_quota=models.IntegerField(default=0)
    date_held=models.DateField()
    time_start=models.TimeField()
    time_finish=models.TimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def decrease_qouta(self):
        with transaction.atomic():
            updated_rows=Schedule.objects.filter(
                id=self.id, remaining_quota__gt=0).update(
                registered_quota=F('registered_quota')+1,
                remaining_quota=F('remaining_quota')-1
            )
            return {"success": updated_rows > 0, "message": "Success Registered." if updated_rows > 0 else "Quota full!"}
    
    def increase_quota(self):
        with transaction.atomic():
            updated_rows=Schedule.objects.filter(
                id=self.id, registered_quota__gt=0).update(
                registered_quota=F('registered_quota')-1,
                remaining_quota=F('remaining_quota')+1
            )
            return {"success": updated_rows > 0, "message": "Success Cancel Course." if updated_rows > 0 else "Cannot Cancel Course"}