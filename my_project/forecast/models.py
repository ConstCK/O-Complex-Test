from django.contrib.auth.models import User
from django.db import models


class ForecastOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    city = models.CharField(max_length=128, verbose_name="Город")
    city_lat = models.FloatField(null=True, verbose_name="Широта")
    city_lon = models.FloatField(null=True, verbose_name="Долгота")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Дата и время запроса")

    def __str__(self):
        return f'{self.city} для {self.user}'

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Запрос прогноза"
        verbose_name_plural = "Запросы прогноза"
