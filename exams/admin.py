from django.contrib import admin
from .models import Exam, ExamQuestion, ExamFavorite


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1
    fields = ('question', 'order', 'code')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'class_obj', 'created_by', 'start_time', 'end_time', 'total_score', 'minutes')
    list_filter = ('start_time', 'end_time', 'created_at', 'class_obj')
    search_fields = ('title', 'description', 'class_obj__className', 'created_by__fullName')
    ordering = ('-created_at',)
    inlines = [ExamQuestionInline]


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('exam', 'question', 'order', 'code')
    list_filter = ('exam', 'order')
    search_fields = ('exam__title', 'question__question_text')
    ordering = ('exam', 'order')


@admin.register(ExamFavorite)
class ExamFavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__fullName', 'exam__title')
    ordering = ('-created_at',)