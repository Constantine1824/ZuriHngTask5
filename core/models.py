from django.db import models


class VideoFile(models.Model):
    file_name = models.CharField(max_length=255)
    temp_file = models.CharField
# Create your models here.
