import mimetypes
import uuid

from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Region(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class District(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Neighborhood(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FileType(models.IntegerChoices):
    IMAGE = 1, 'Image'
    VIDEO = 2, 'Video'
    DOCUMENT = 3, 'Document'
    AUDIO = 4, 'Audio'
    OTHER = 5, 'Other'


class Media(BaseModel):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    file = models.FileField(upload_to='media/')
    file_type = models.IntegerField(choices=FileType.choices, default=FileType.OTHER)
    file_name = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name

        if self.file:
            content_type, _ = mimetypes.guess_type(self.file.name)
            if content_type:
                main_type = content_type.split('/')[0]
                if main_type == 'image':
                    self.file_type = FileType.IMAGE
                elif main_type == 'video':
                    self.file_type = FileType.VIDEO
                elif main_type == 'audio':
                    self.file_type = FileType.AUDIO
                elif main_type in ['application', 'text']:
                    self.file_type = FileType.DOCUMENT
                else:
                    self.file_type = FileType.OTHER
            else:
                self.file_type = FileType.OTHER

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.file.name}"
