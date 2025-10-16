from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('admin', 'Admin'),
    ]
    
    fullName = models.CharField(max_length=255, verbose_name="Full Name")
    email = models.EmailField(unique=True, verbose_name="Email")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student', verbose_name="Role")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Last Login")
    
    # Override username field to use email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullName']
    
    class Meta:
        db_table = 'users'
        verbose_name = "User"
        verbose_name_plural = "Users"
    
    def __str__(self):
        return f"{self.fullName} ({self.email})"
    
    def save(self, *args, **kwargs):
        # Set username to email if not provided
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)