from django.db import models

from src.user.models import User


class TikTokUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tiktok_username = models.CharField(max_length=100)


class TikTokVideo(models.Model):
    STATUS_UPLOADED = 'uploaded'

    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=20)
