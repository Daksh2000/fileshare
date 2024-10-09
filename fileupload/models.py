# fileupload/models.py
from django.db import models
from django.contrib.auth.models import User
import uuid


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files')
    title = models.CharField(max_length=100)
    description = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    file = models.FileField(upload_to='user_files/')
    file_type = models.CharField(max_length=50, blank=True, null=True)
    compressed = models.BooleanField(default=False)
    public_url = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.title} uploaded by {self.user.username}'

    def generate_public_url(self):
        if not self.public_url:
            self.public_url = str(uuid.uuid4())[:8]
        self.save()
