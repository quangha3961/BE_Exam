from django.contrib import admin
from .models import Class, ClassStudent


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('className', 'teacher', 'created_at')
    list_filter = ('created_at', 'teacher')
    search_fields = ('className', 'teacher__fullName', 'teacher__email')
    ordering = ('-created_at',)


@admin.register(ClassStudent)
class ClassStudentAdmin(admin.ModelAdmin):
    list_display = ('class_obj', 'student', 'joined_at')
    list_filter = ('joined_at', 'class_obj')
    search_fields = ('class_obj__className', 'student__fullName', 'student__email')
    ordering = ('-joined_at',)