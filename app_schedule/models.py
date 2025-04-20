import redis
from django.db import models, transaction
from django.db.models import F
from django.core.cache import cache 
from app_course.models import Course
from app_building.models import Building, Room
from app_staff.models import TeachingStaff
from app_student.models import Student 
from app_common.models import  Term, Department, Faculty

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
    
    DAYS_OF_WEEK = [
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
        ('Minggu', 'Minggu'),
    ]
    
    semester_pack=models.IntegerField(choices=semester_choices, default=1)
    course=models.OneToOneField(Course, on_delete=models.CASCADE, related_name='schedules')
    building=models.ForeignKey(Building, on_delete=models.CASCADE, related_name='schedules')
    room=models.ForeignKey(Room, on_delete=models.CASCADE, related_name='schedules')
    teaching_staff=models.ForeignKey(TeachingStaff, on_delete=models.CASCADE, related_name='schedules')
    department=models.ForeignKey(Department, on_delete=models.CASCADE, related_name='schedules')
    max_quota=models.PositiveIntegerField()
    remaining_quota=models.PositiveIntegerField(default=0)
    registered_quota=models.PositiveIntegerField(default=0)
    day_held=models.CharField(max_length=6, choices=DAYS_OF_WEEK)
    time_start=models.TimeField()
    time_finish=models.TimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if self.pk is None:  # Hanya pertama kali dibuat
            self.remaining_quota = self.max_quota
        super().save(*args, **kwargs)
        # redis_client.set(self.get_redis_key(), self.remaining_quota, ex=60)
    
    def __str__(self):
        return f"{self.id}-{self.course}"
    
class RegisteredSchedule(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name="register_schedule")
    schedule=models.ManyToManyField(Schedule, related_name="register_schedule")
    term=models.ForeignKey(Term, on_delete=models.CASCADE, related_name="register_schedule")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def update_schedule(self, new_schedule_ids):
        """
        Update registered schedules and adjust quota accordingly.
        """
        cache_key = f"student_{self.student.id}_term_{self.term.id}_schedules"
        cached_schedules = cache.get(cache_key)
        
        if cached_schedules is None:
            old_schedules = set(self.schedule.values_list("id", flat=True))
            cache.set(cache_key, list(old_schedules), timeout=300)
        else:
            old_schedules = set(cached_schedules)

        new_schedules = set(new_schedule_ids)
        to_add = new_schedules - old_schedules
        to_remove = old_schedules - new_schedules

        if to_add:
            self.schedule.add(*to_add)
            Schedule.objects.filter(id__in=to_add).update(
                remaining_quota=F("remaining_quota") - 1,
                registered_quota=F("registered_quota") + 1
            )
        
        if to_remove:
            self.schedule.remove(*to_remove)
            Schedule.objects.filter(id__in=to_remove).update(
                remaining_quota=F("remaining_quota") + 1,
                registered_quota=F("registered_quota") - 1
            )
        
        cache.set(cache_key, list(new_schedules), timeout=300)
        
    def __str__(self):
        return f"{self.id}-{self.student.nim}"