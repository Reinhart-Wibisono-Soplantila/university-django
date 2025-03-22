import redis
from django.db import models, transaction
from django.db.models import F
from django.core.cache import cache
from app_course.models import Course
from app_building.models import Building, Room
from app_staff.models import TeachingStaff

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)
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
    remaining_quota=models.IntegerField(default=0)
    registered_quota=models.IntegerField(default=0)
    date_held=models.DateField()
    time_start=models.TimeField()
    time_finish=models.TimeField()
    datetime_reset=models.DateField()
    registered_until=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def get_redis_key(self):
        return f"schedule_quota:{self.id}"
    
    def get_remaining_quota(self):
        key = self.get_redis_key()
        quota = redis_client.get(key)
        if quota is None:
            quota = self.remaining_quota
            redis_client.set(key, quota, ex=60)
        return int(quota)
    
    def decrease_quota(self):
        key = self.get_redis_key()
        lock_key = f"lock:{key}"

        with redis_client.lock(lock_key, timeout=5):  # Lock selama 5 detik
            remaining_quota = self.get_remaining_quota()

            if remaining_quota <= 0:
                return {"success": False, "message": "Quota full!"}

            with transaction.atomic():
                updated_rows = Schedule.objects.filter(
                    id=self.id, remaining_quota__gt=0
                ).update(
                    registered_quota=F('registered_quota') + 1,
                    remaining_quota=F('remaining_quota') - 1
                )

                if updated_rows > 0:
                    redis_client.decr(key)

                return {
                    "success": bool(updated_rows),
                    "message": "Success Registered." if updated_rows > 0 else "Quota full!"
                }
    
    def increase_quota(self):
        key = self.get_redis_key()
        lock_key = f"lock:{key}"

        with redis_client.lock(lock_key, timeout=5):  # Lock selama 5 detik
            with transaction.atomic():
                updated_rows = Schedule.objects.filter(
                    id=self.id, registered_quota__gt=0
                ).update(
                    registered_quota=F('registered_quota') - 1,
                    remaining_quota=F('remaining_quota') + 1
                )

                if updated_rows > 0:
                    redis_client.incr(key)  # Tambah quota di Redis

                return {
                    "success": bool(updated_rows),
                    "message": "Success Cancel Course." if updated_rows > 0 else "Cannot Cancel Course"
                }
    
    def save(self, *args, **kwargs):
        if self.pk is None:  # Hanya pertama kali dibuat
            self.remaining_quota = self.max_quota
        super().save(*args, **kwargs)
        redis_client.set(self.get_redis_key(), self.remaining_quota, ex=60)