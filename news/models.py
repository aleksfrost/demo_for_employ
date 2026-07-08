from django.db import models
from django.utils import timezone
import os
from io import BytesIO
from django.core.files.base import ContentFile
from PIL import Image
from tinymce.models import HTMLField

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Тег")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        

class News(models.Model):
    """Модель новости из Telegram"""
    telegram_message_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        verbose_name="ID сообщения в TG"
    )
    title = models.CharField(
        max_length=500,
        verbose_name="Заголовок новости"
    )

    content = HTMLField(
        verbose_name="Текст новости"
    )

    preview = HTMLField(
        max_length=300,
        blank=True,
        verbose_name="Превью (кратко)",
        help_text="Если оставить пустым, в ленте покажутся первые 200 символов текста."
    )

    # Обычное поле для картинки
    image = models.ImageField(
        upload_to='news/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Автоматически сжимается и создаётся миниатюра для ленты."
    )

    image_credit = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Автор / источник",
        help_text="Например: фото: Иван Иванов, источник: unsplash.com"
    )

    image_source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на источник",
        help_text="Если указана, ссылка появится под картинкой"
    )

    # Миниатюра для ленты
    thumbnail = models.ImageField(
        upload_to='news/thumbnails/%Y/%m/%d/',
        blank=True,
        null=True,
        editable=False
    )

    published_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата публикации"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Добавлено на сайт"
    )
    views_count = models.IntegerField(
        default=0,
        verbose_name="Просмотры"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Снимите галочку, чтобы скрыть новость с сайта."
    )
    
    is_important = models.BooleanField(
        default=False, 
        verbose_name="Важный заголовок (жирный в правой колонке)", 
        help_text="Поставьте галочку, чтобы выделить жирным справа."
    )

    reactions = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Реакции (эмодзи)"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        verbose_name="ЧПУ (slug)",
        blank=True,
        help_text="Часть URL после /news/. Если не заполнить — создастся автоматически из заголовка. Пример: «itogi-rynka-fevral-2026»"
    )
    
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='news',
        verbose_name="Теги"
    )
    
    video_url = models.TextField(
        blank=True, 
        null=True, 
        verbose_name="Код iframe для видео"
    )

    # SEO-поля
    meta_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Meta Title (если пусто = заголовок)",
        help_text="Заголовок для поисковых систем (то, что видно в выдаче). Если не заполнить — возьмется из обычного заголовка. Пример: «Итоги рынка апартаментов за февраль 2026 | apartprofi»"
    )
    meta_description = models.TextField(
        max_length=300,
        blank=True,
        verbose_name="Meta Description",
        help_text="Краткое описание (150-200 символов) — показывается в поиске под заголовком. Если не заполнить — поисковик сам возьмет кусок текста. Пример: «Аналитика рынка апартаментов: средняя цена, спрос, новые ЖК. Данные по Москве и СПб за февраль 2026.»"
    )
    meta_keywords = models.CharField(
        max_length=250,
        blank=True,
        verbose_name="Meta Keywords (через запятую)",
        help_text="Ключевые слова через запятую. Пример: «апартаменты, рынок недвижимости, аналитика, новостройки, инвестиции»"
    )
    h1_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="H1 заголовок (если пусто = заголовок)",
        help_text="Заголовок на странице новости. Если не заполнить — будет использован обычный заголовок. Пример: «Итоги рынка апартаментов за февраль 2026»"
    )
    is_index = models.BooleanField(
        default=True,
        verbose_name="Разрешить индексацию",
        help_text="Если снять галочку — страница будет закрыта от индексации (noindex). Обычно оставляем включенным."
    )

    attachment = models.FileField(
        upload_to='attachments/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="Вложение (PDF, таблица и т.д.)",
        help_text="Файл для скачивания (необязательно)"
    )

    class Meta:
        ordering = ['-published_at']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title[:50]

    def get_reactions(self):
        return self.reactions or {}

    def add_reaction(self, emoji):
        if not self.reactions:
            self.reactions = {}
        self.reactions[emoji] = self.reactions.get(emoji, 0) + 1
        self.save(update_fields=['reactions'])

    def remove_reaction(self, emoji):
        if self.reactions and emoji in self.reactions:
            self.reactions[emoji] -= 1
            if self.reactions[emoji] <= 0:
                del self.reactions[emoji]
            self.save(update_fields=['reactions'])

    def get_meta_title(self):
        return self.meta_title or self.title

    def get_h1(self):
        return self.h1_title or self.title

    def save(self, *args, **kwargs):
        # Автоматическое формирование slug из title, если не заполнен
        if not self.slug and self.title:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            self.slug = base_slug
            counter = 1
            while News.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1

        # Сначала сохраняем, чтобы у image появился путь
        super().save(*args, **kwargs)

        # Обработка картинки и создание миниатюры
        if self.image:
            try:
                # Открываем оригинал
                img = Image.open(self.image.path)

                # Сжимаем и ресайзим оригинал (если нужно)
                if img.height > 800 or img.width > 1200:
                    output_size = (1200, 800)
                    img.thumbnail(output_size, Image.Resampling.LANCZOS)

                # Сохраняем сжатый оригинал
                img.save(self.image.path, quality=85, optimize=True)

                # Создаём миниатюру для ленты (всегда заново)
                thumb = Image.open(self.image.path)
                thumb.thumbnail((600, 400), Image.Resampling.LANCZOS)

                # Сохраняем миниатюру
                thumb_io = BytesIO()
                thumb.save(thumb_io, format='JPEG', quality=95, optimize=False)
                thumb_filename = f"{os.path.basename(self.image.name).split('.')[0]}_thumb.jpg"

                # Если миниатюра уже есть — удаляем старую
                if self.thumbnail:
                    self.thumbnail.delete(save=False)

                self.thumbnail.save(thumb_filename, ContentFile(thumb_io.getvalue()), save=False)

                # Финальное сохранение
                super().save(update_fields=['thumbnail'])

            except Exception as e:
                print(f"Ошибка обработки изображения: {e}")
                
    def get_related_news(self, limit=5):
        if not self.tags.exists():
            return News.objects.none()
        
        return News.objects.filter(
            tags__in=self.tags.all(),
            is_active=True
        ).exclude(pk=self.pk).distinct().order_by('-published_at')[:limit]


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='news/%Y/%m/%d/', verbose_name="Изображение")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Подпись")
    order = models.IntegerField(default=0, verbose_name="Порядок")


    credit = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Автор / источник",
        help_text="Например: фото: Иван Иванов"
    )

    source_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="Ссылка на источник"
    )

    class Meta:
        ordering = ['order']
        verbose_name = "Изображение"
        verbose_name_plural = "Изображения"

    def __str__(self):
        return f"Изображение к {self.news.title[:30]}"