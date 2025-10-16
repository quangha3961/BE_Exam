from django.db import models
from django.conf import settings
from exams.models import Exam


class Notification(models.Model):
    """
    Model representing notifications for users
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications',
        verbose_name="User"
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    is_read = models.BooleanField(default=False, verbose_name="Is Read")
    related_exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='notifications',
        verbose_name="Related Exam"
    )
    
    class Meta:
        db_table = 'notifications'
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.fullName} - {self.title}"