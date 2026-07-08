from django.db import models

class SiteSettings(models.Model):
    logo = models.ImageField(upload_to='logo/', blank=True, null=True, verbose_name="Логотип")
    favicon = models.ImageField(upload_to='favicon/', blank=True, null=True, verbose_name="Иконка (favicon)")
    comments_enabled = models.BooleanField(default=True, verbose_name="Комментарии включены")
    headlines_count = models.IntegerField(default=15, verbose_name="Количество заголовков в правой колонке")

    class Meta:
        verbose_name = "Настройки сайта"
        verbose_name_plural = "Настройки сайта"

    def __str__(self):
        return "Настройки сайта"