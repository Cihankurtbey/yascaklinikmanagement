from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'notification_type', 'recipient_phone', 'status', 'sent_at', 'created_at')
    list_filter = ('status', 'notification_type', 'created_at')
    search_fields = ('recipient_phone', 'message')
    readonly_fields = ('sent_at', 'created_at')
