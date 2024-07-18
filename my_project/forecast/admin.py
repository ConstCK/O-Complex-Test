from django.contrib import admin

from .models import ForecastOrder


class ForecastAdmin(admin.ModelAdmin):
    fields = ['user', 'city', 'city_lat', 'city_lon', 'created_at']
    readonly_fields = ['created_at']


admin.site.register(ForecastOrder, ForecastAdmin)



