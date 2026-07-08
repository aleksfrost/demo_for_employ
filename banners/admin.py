from django.contrib import admin
from .models import Banner

@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active', 'views_count', 'clicks_count')
    list_filter = ('position', 'is_active')
    search_fields = ('name', 'title', 'text')

    fieldsets = (
        ('Основное', {
            'fields': ('name', 'position', 'order', 'is_active'),
        }),
        ('Контент', {
            'fields': ('title', 'text', 'image', 'url'),
        }),
        ('Статистика', {
            'fields': ('views_count', 'clicks_count'),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = ('views_count', 'clicks_count')