from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username
    
    class Meta:
        db_table = 'auth_user'


class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    public_key_pem = models.TextField()

    def __str__(self):
        return f"{self.device_id}"
    
    class Meta:
        db_table = 'user_devices'
