from django.contrib import admin
from .models import Question, QuestionAnswer


class QuestionAnswerInline(admin.TabularInline):
    model = QuestionAnswer
    extra = 1
    fields = ('text', 'is_correct')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'teacher', 'type', 'difficulty', 'created_at')
    list_filter = ('type', 'difficulty', 'created_at', 'teacher')
    search_fields = ('question_text', 'teacher__fullName')
    ordering = ('-created_at',)
    inlines = [QuestionAnswerInline]


@admin.register(QuestionAnswer)
class QuestionAnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct', 'created_at')
    list_filter = ('is_correct', 'created_at')
    search_fields = ('text', 'question__question_text')
    ordering = ('-created_at',)