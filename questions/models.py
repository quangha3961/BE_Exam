from django.db import models
from django.conf import settings


class Question(models.Model):
    """
    Model representing a question
    """
    TYPE_CHOICES = [
        ('multiple_choice', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('fill_blank', 'Fill in the Blank'),
        ('essay', 'Essay'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='created_questions',
        verbose_name="Teacher"
    )
    question_text = models.TextField(verbose_name="Question Text")
    image_url = models.URLField(blank=True, null=True, verbose_name="Image URL")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='multiple_choice', verbose_name="Type")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium', verbose_name="Difficulty")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        db_table = 'questions'
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.question_text[:50]}... - {self.teacher.fullName}"


class QuestionAnswer(models.Model):
    """
    Model representing answers for a question
    """
    question = models.ForeignKey(
        Question, 
        on_delete=models.CASCADE, 
        related_name='answers',
        verbose_name="Question"
    )
    text = models.TextField(verbose_name="Answer Text")
    is_correct = models.BooleanField(default=False, verbose_name="Is Correct")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        db_table = 'question_answers'
        verbose_name = "Question Answer"
        verbose_name_plural = "Question Answers"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.text[:30]}... - {'✓' if self.is_correct else '✗'}"