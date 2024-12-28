from django.db import models
from django.contrib.auth.models import User

class TelegramSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    session_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
