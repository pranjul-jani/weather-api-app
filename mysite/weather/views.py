from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests


# Create your views here.
def index(request):
    api_key = 'bfdc41ce2c648b95838eb8f814f97256'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm

    cities = City.objects.all()[:10]
    weather_data = []

    for city in cities:
        # this is the response, and by .json we are converting it to python dictionary
        r = requests.get(url.format(city, api_key)).json()
        # since the temp in kelvin we are converting it to celsius
        temp_in_celsius = str(int(float(r['main']['temp']) - 273.15))

        # we only need the weather description, the icon, the city and the temperature
        city_weather = {
            'city': city.name,
            'temperature': temp_in_celsius,
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data,
               'form': form}

    return render(request, 'weather/weather.html', context)
