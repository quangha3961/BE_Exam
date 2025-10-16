from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'is_read', 'related_exam', 'created_at')
    list_filter = ('is_read', 'created_at', 'related_exam')
    search_fields = ('user__fullName', 'title', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)