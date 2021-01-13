import requests
from django.shortcuts import render
from .models import City
from .forms import CityForm


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=[YOUR KEY]'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()

    cities = City.objects.all()

    weatherData = []

    for city in cities:
        req = requests.get(url.format(city)).json()

        cityWeather = {
            'city': city.name,
            'temperature': req['main']['temp'],
            'feels': req['main']['feels_like'],
            'description': req['weather'][0]['description'].capitalize(),
            'humidity': req['main']['humidity'],
            'icon': req['weather'][0]['icon'],
        }

        weatherData.append(cityWeather)

    context = {'weatherData': weatherData, 'form': form}

    return render(request, 'weather/weather.html', context)
