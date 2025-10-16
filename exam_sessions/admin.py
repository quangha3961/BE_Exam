from django.contrib import admin
from .models import ExamSession, StudentAnswer, ExamResult, ExamLog


class StudentAnswerInline(admin.TabularInline):
    model = StudentAnswer
    extra = 0
    fields = ('exam_question', 'selected_answer', 'answer_text', 'score', 'is_correct')
    readonly_fields = ('answered_at',)


class ExamLogInline(admin.TabularInline):
    model = ExamLog
    extra = 0
    fields = ('actions', 'timestamp', 'detail')
    readonly_fields = ('timestamp',)


@admin.register(ExamSession)
class ExamSessionAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'status', 'start_time', 'end_time', 'total_score')
    list_filter = ('status', 'start_time', 'exam')
    search_fields = ('student__fullName', 'exam__title', 'code')
    ordering = ('-start_time',)
    inlines = [StudentAnswerInline, ExamLogInline]


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ('session', 'exam_question', 'selected_answer', 'score', 'is_correct', 'answered_at')
    list_filter = ('is_correct', 'answered_at')
    search_fields = ('session__student__fullName', 'session__exam__title')
    ordering = ('-answered_at',)


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'total_score', 'percentage', 'correct_count', 'wrong_count', 'status')
    list_filter = ('status', 'submitted_at')
    search_fields = ('student__fullName', 'exam__title')
    ordering = ('-submitted_at',)


@admin.register(ExamLog)
class ExamLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'actions', 'timestamp')
    list_filter = ('actions', 'timestamp')
    search_fields = ('student__fullName', 'session__exam__title', 'actions')
    ordering = ('-timestamp',)