from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
import dotenv
import os

dotenv.load_dotenv()


def index(request):

    url = "https://api.openweathermap.org/data/2.5/weather?"

    if request.method == "POST":
        form = CityForm(request.POST)
        form.save()

    form = CityForm()
    cities = City.objects.all()
    all_cities = []

    for city in cities:
        params = {
            "q": city.name,
            "units": "metric",
            "appid": os.getenv("WEATHER_APP_ID"),
        }
        response = requests.get(url=url, params=params).json()
        city_info = {
            'city': city.name,
            'temp': response["main"]["temp"],
            'icon': response["weather"][0]["icon"],
        }
        all_cities.append(city_info)
    context = {'all_info': all_cities, 'form': form}

    return render(request, 'weather/index.html', context)


