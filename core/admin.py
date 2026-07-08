from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    # core/admin.py
    fields = ('logo', 'favicon', 'comments_enabled', 'headlines_count')