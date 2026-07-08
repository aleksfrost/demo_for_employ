from django.contrib import admin
from .models import News, NewsImage, Tag

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ('image', 'caption', 'credit', 'source_url', 'order')
    ordering = ('order',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'views_count', 'is_active', 'is_index')
    list_filter = ('is_active', 'is_index', 'published_at')
    search_fields = ('title', 'content', 'meta_title', 'meta_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline]

    fieldsets = (
        ('Основное', {
            'fields': ('title', 'content', 'preview', 'image', 'image_credit', 'image_source_url', 'attachment', 'is_important', 'published_at', 'is_active'),
        }),
        ('SEO-настройки', {
            'fields': ('slug', 'h1_title', 'meta_title', 'meta_description', 'meta_keywords', 'is_index', 'tags'),
            'classes': ('wide',),
        }),
        ('Статистика', {
            'fields': ('views_count', 'reactions', 'telegram_message_id'),
            'classes': ('collapse',),
        }),
        ('Видео', {
            'fields': ('video_url',),
            'classes': ('collapse',),
        }),
    )
    
    filter_horizontal = ('tags',)

    readonly_fields = ('views_count', 'reactions')

    actions = ['make_active', 'make_inactive', 'make_index', 'make_noindex']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = "Опубликовать выбранные новости"

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = "Снять с публикации"

    def make_index(self, request, queryset):
        queryset.update(is_index=True)
    make_index.short_description = "Разрешить индексацию"

    def make_noindex(self, request, queryset):
        queryset.update(is_index=False)
    make_noindex.short_description = "Запретить индексацию (noindex)"