import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from apps.common.models import BaseModel


class Gender(models.IntegerChoices):
    FEMALE = 0, "Female"
    MALE = 1, "Male"


class RoleType(models.IntegerChoices):
    STUDENT = 1, "Student"
    TEACHER = 2, "Teacher"
    RECTOR = 3, "Rector"


class User(AbstractUser, BaseModel):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    middle_name = models.CharField(max_length=150, blank=True)
    phone1 = PhoneNumberField(null=True, unique=True, db_index=True)
    phone2 = PhoneNumberField(null=True, unique=True, db_index=True)
    role = models.IntegerField(choices=RoleType.choices, default=RoleType.STUDENT)
    gender = models.IntegerField(choices=Gender.choices, null=True)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name} {self.middle_name}"

    class Meta:
        ordering = ("last_name", "first_name")


class UserDevice(BaseModel):
    user = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True)
    device_name = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    refresh_token = models.TextField()
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.device_name}"

class UserActivity(models.Model):
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    date = models.DateField()
    active_time = models.DurationField(default=timedelta(seconds=0))

    class Meta:
        unique_together = ("user", "date")  # bir kunda 1 ta yozuv
        verbose_name = "User Activity"
        verbose_name_plural = "User Activities"

    def __str__(self):
        return f"{self.user} - {self.date} ({self.active_time}s)"
