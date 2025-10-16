from django.db import models
from django.conf import settings
from classes.models import Class
from questions.models import Question


class Exam(models.Model):
    """
    Model representing an exam
    """
    class_obj = models.ForeignKey(
        Class, 
        on_delete=models.CASCADE, 
        related_name='exams',
        verbose_name="Class"
    )
    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    total_score = models.PositiveIntegerField(default=100, verbose_name="Total Score")
    minutes = models.PositiveIntegerField(verbose_name="Duration (minutes)")
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(verbose_name="End Time")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_exams',
        verbose_name="Created By"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        db_table = 'exams'
        verbose_name = "Exam"
        verbose_name_plural = "Exams"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.class_obj.className}"


class ExamQuestion(models.Model):
    """
    Model representing the many-to-many relationship between exams and questions
    """
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='exam_questions',
        verbose_name="Exam"
    )
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='exam_questions',
        verbose_name="Question"
    )
    order = models.PositiveIntegerField(verbose_name="Order")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code")
    
    class Meta:
        db_table = 'exam_questions'
        verbose_name = "Exam Question"
        verbose_name_plural = "Exam Questions"
        unique_together = ['exam', 'question']
        ordering = ['order']
    
    def __str__(self):
        return f"{self.exam.title} - Q{self.order}: {self.question.question_text[:30]}..."


class ExamFavorite(models.Model):
    """
    Model representing user's favorite exams
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='favorite_exams',
        verbose_name="User"
    )
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='favorites',
        verbose_name="Exam"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        db_table = 'exam_favorites'
        verbose_name = "Exam Favorite"
        verbose_name_plural = "Exam Favorites"
        unique_together = ['user', 'exam']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.fullName} favorites {self.exam.title}"