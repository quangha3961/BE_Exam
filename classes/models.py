from django.db import models
from django.conf import settings


class Class(models.Model):
    """
    Model representing a class/classroom
    """
    className = models.CharField(max_length=255, verbose_name="Class Name")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='taught_classes',
        verbose_name="Teacher"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        db_table = 'classes'
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.className} - {self.teacher.fullName}"


class ClassStudent(models.Model):
    """
    Model representing the many-to-many relationship between classes and students
    """
    class_obj = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='students',
        verbose_name="Class"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='enrolled_classes',
        verbose_name="Student"
    )
    joined_at = models.DateTimeField(auto_now_add=True, verbose_name="Joined At")
    
    class Meta:
        db_table = 'class_students'
        verbose_name = "Class Student"
        verbose_name_plural = "Class Students"
        unique_together = ['class_obj', 'student']
        ordering = ['-joined_at']
    
    def __str__(self):
        return f"{self.student.fullName} in {self.class_obj.className}"