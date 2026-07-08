from django.db import models

class Banner(models.Model):
    POSITION_CHOICES = [
        ('left', 'Левая колонка - аналитика'),
        ('right', 'Правая колонка - реклама'),
        ('center_top', 'Центральная колонка - первая новость'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Название (только для админки)"
    )

    position = models.CharField(
        max_length=20,
        choices=POSITION_CHOICES,
        default='right',
        verbose_name="Позиция",
        help_text="Слева — аналитика (графики, статистика). Справа — реклама или ссылки."
    )

    # Контент
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Заголовок",
        help_text="Необязательно. Если есть картинка — будет под ней."
    )

    text = models.TextField(
        blank=True,
        verbose_name="Текст",
        help_text="Необязательно. Описание под заголовком (или отдельно, если заголовка нет)."
    )

    image = models.ImageField(
        upload_to='banners/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Для графиков или рекламных картинок."
    )

    url = models.URLField(
        blank=True,
        verbose_name="Ссылка",
        help_text="Куда перейдёт пользователь при клике на баннер или кнопку 'Подробнее'."
    )

    # Управление
    order = models.IntegerField(
        default=0,
        verbose_name="Порядок",
        help_text="Чем меньше число, тем выше в колонке."
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        help_text="Снимите галочку, чтобы скрыть баннер с сайта."
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создан")

    # Счетчики для рекламы (как ты и сказал)
    views_count = models.IntegerField(
        default=0,
        verbose_name="Показы",
        help_text="Сколько раз баннер показан пользователям (обновляется автоматически)."
    )

    clicks_count = models.IntegerField(
        default=0,
        verbose_name="Клики",
        help_text="Сколько раз кликнули по ссылке (обновляется автоматически)."
    )

    class Meta:
        ordering = ['position', 'order']
        verbose_name = "Баннер"
        verbose_name_plural = "Баннеры"

    def __str__(self):
        return f"{self.get_position_display()}: {self.name}"

    def get_position_display(self):
        return dict(self.POSITION_CHOICES).get(self.position, self.position)