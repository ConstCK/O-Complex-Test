from django.urls import path
from .views import main, statistic, about

urlpatterns = [
    path('', main, name='main'),
    path('statistic/', statistic, name='statistic'),
    path('about/', about, name='about'),
]
