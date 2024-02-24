from django.db import models
from .manager import UserManager
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.TextField(null=True, blank = True)
    phone_no = models.TextField(null=True, blank = True)
    get_email_notification = models.BooleanField(default=True)
    USERNAME_FIELD =  'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    objects = UserManager()

class OtpObject(models.Model):
    
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_valid = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.email} - {self.otp}'
    
    def is_valid_otp(self):
        if self.is_valid and (timezone.now() - self.created_at).seconds < 300:
            return True
        return False