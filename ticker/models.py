from django.db import models
from tinymce.models import HTMLField

class Ticker(models.Model):
    content = HTMLField(verbose_name="Текст бегущей строки")
    speed = models.IntegerField(default=60, verbose_name="Скорость (секунды)", help_text="Чем меньше число, тем быстрее бежит строка")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        verbose_name = "Бегущая строка"
        verbose_name_plural = "Бегущая строка"

    def __str__(self):
        return "Бегущая строка"