import requests
from django.contrib.auth.models import User
from django.shortcuts import render
from .forms import ForecastOrderForm
from .models import ForecastOrder
from .services import (get_coords_by_city,
                       get_coords_from_db,
                       get_weather_forecast,
                       add_data_to_db,
                       last_city_info)


def main(request):
    try:
        user = User.objects.get(username=request.user)
        last_city = last_city_info(user)
    except Exception:
        last_city = ''
    finally:
        form = ForecastOrderForm({'city': last_city})


    if request.method == "POST":
        form = ForecastOrderForm(request.POST)
        if form.is_valid():

            city = request.POST.get('city')
            # Проверка есть ли координаты города в БД и добавление нового запроса
            if get_coords_from_db(city):
                result = get_weather_forecast(str(get_coords_from_db(city).get('latitude')),
                                              str(get_coords_from_db(city).get('longitude')))
                add_data_to_db(user,
                               city,
                               get_coords_from_db(city).get('latitude'),
                               get_coords_from_db(city).get('longitude'))

            else:
                coords = get_coords_by_city(city)
                lat = coords.get('latitude')
                lon = coords.get('longitude')
                result = get_weather_forecast(lat, lon)
                print(result)

                add_data_to_db(user,
                               city,
                               lat,
                               lon)

            return render(request,
                          'main.html',
                          context={'city': city,
                                   'hour': result.get('hour'),
                                   'temperature': result.get('temperature'),
                                   'form': form})

    return render(request, 'main.html',
                  context={'form': form})


def statistic(request):
    return render(request, 'main.html', context={})


def about(request):
    return render(request, 'main.html', context={})
