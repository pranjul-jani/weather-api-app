from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm
import requests


# Create your views here.
def index(request):
    api_key = 'bfdc41ce2c648b95838eb8f814f97256'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={0}&appid={1}'

    error_msg = ''
    message = ''
    message_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            # this is the response, and by .json we are converting it to python dictionary
            r = requests.get(url.format(new_city, api_key)).json()
            if r['cod'] == 200:
                form.save()
            else:
                error_msg = 'City does not exist in the world'
        else:
            error_msg = 'City already exists in the database!'

        if error_msg:
            message = error_msg
            message_class = 'is-danger'

        else:
            message = 'City added successfully'
            message_class = 'is-success'

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
               'form': form,
               'message': message,
               'message_class': message_class,
               }

    return render(request, 'weather/weather.html', context)


def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')



