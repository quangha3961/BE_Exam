from django.db import models
from django.conf import settings
from exams.models import Exam, ExamQuestion
from questions.models import QuestionAnswer


class ExamSession(models.Model):
    """
    Model representing a student's exam session
    """
    STATUS_CHOICES = [
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('abandoned', 'Abandoned'),
        ('timeout', 'Timeout'),
    ]
    
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='sessions',
        verbose_name="Exam"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='exam_sessions',
        verbose_name="Student"
    )
    code = models.CharField(max_length=50, unique=True, verbose_name="Session Code")
    start_time = models.DateTimeField(verbose_name="Start Time")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="End Time")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Total Score")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name="Status")
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Submitted At")
    
    class Meta:
        db_table = 'exam_sessions'
        verbose_name = "Exam Session"
        verbose_name_plural = "Exam Sessions"
        unique_together = ['exam', 'student']
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.student.fullName} - {self.exam.title} ({self.status})"


class StudentAnswer(models.Model):
    """
    Model representing a student's answer to a question
    """
    session = models.ForeignKey(
        ExamSession, 
        on_delete=models.CASCADE, 
        related_name='answers',
        verbose_name="Session"
    )
    exam_question = models.ForeignKey(
        ExamQuestion, 
        on_delete=models.CASCADE, 
        related_name='student_answers',
        verbose_name="Exam Question"
    )
    selected_answer = models.ForeignKey(
        QuestionAnswer, 
        on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='student_selections',
        verbose_name="Selected Answer"
    )
    answer_text = models.TextField(blank=True, null=True, verbose_name="Answer Text")
    score = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Score")
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="Answered At")
    is_correct = models.BooleanField(default=False, verbose_name="Is Correct")
    
    class Meta:
        db_table = 'student_answers'
        verbose_name = "Student Answer"
        verbose_name_plural = "Student Answers"
        unique_together = ['session', 'exam_question']
        ordering = ['exam_question__order']
    
    def __str__(self):
        return f"{self.session.student.fullName} - Q{self.exam_question.order} - {'✓' if self.is_correct else '✗'}"


class ExamResult(models.Model):
    """
    Model representing the final result of an exam session
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('graded', 'Graded'),
        ('reviewed', 'Reviewed'),
    ]
    
    session = models.OneToOneField(
        ExamSession, 
        on_delete=models.CASCADE, 
        related_name='result',
        verbose_name="Session"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='exam_results',
        verbose_name="Student"
    )
    exam = models.ForeignKey(
        Exam, 
        on_delete=models.CASCADE, 
        related_name='results',
        verbose_name="Exam"
    )
    total_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Total Score")
    correct_count = models.PositiveIntegerField(verbose_name="Correct Count")
    wrong_count = models.PositiveIntegerField(verbose_name="Wrong Count")
    submitted_at = models.DateTimeField(verbose_name="Submitted At")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    feedback = models.TextField(blank=True, null=True, verbose_name="Feedback")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Percentage")
    
    class Meta:
        db_table = 'exam_results'
        verbose_name = "Exam Result"
        verbose_name_plural = "Exam Results"
        ordering = ['-submitted_at']
    
    def __str__(self):
        return f"{self.student.fullName} - {self.exam.title} - {self.percentage}%"


class ExamLog(models.Model):
    """
    Model representing logs of student actions during exam
    """
    session = models.ForeignKey(
        ExamSession, 
        on_delete=models.CASCADE, 
        related_name='logs',
        verbose_name="Session"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='exam_logs',
        verbose_name="Student"
    )
    actions = models.CharField(max_length=100, verbose_name="Action")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")
    detail = models.TextField(blank=True, null=True, verbose_name="Detail")
    
    class Meta:
        db_table = 'exam_logs'
        verbose_name = "Exam Log"
        verbose_name_plural = "Exam Logs"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.student.fullName} - {self.actions} - {self.timestamp}"