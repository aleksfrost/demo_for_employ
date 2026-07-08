from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'news', 'created_at', 'is_banned')
    list_filter = ('is_banned', 'created_at')
    search_fields = ('user__username', 'text')
    actions = ['ban_comments', 'unban_comments']

    def ban_comments(self, request, queryset):
        queryset.update(is_banned=True)
    ban_comments.short_description = "Забанить выбранные комментарии"

    def unban_comments(self, request, queryset):
        queryset.update(is_banned=False)
    unban_comments.short_description = "Разбанить выбранные комментарии"