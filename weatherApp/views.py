import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.core.cache import cache
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from .models import CityWeatherData, User


def update():
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'San Francisco', 'Charlotte', 'Indianapolis', 'Seattle', 'Denver', 'Washington', 'Boston', 'Nashville', 'El Paso', 'Detroit', 'Memphis', 'Portland', 'Oklahoma City', 'Las Vegas', 'Louisville', 'Baltimore']
    for city in cities:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=3ac3c441a33320613634b943eca4199a'
        r = requests.get(url).json()
        if r.get('cod') == 200:
            country_code = r['sys']['country']
            coordinate = [r['coord']['lat'], r['coord']['lon']]
            temp = r['main']['temp']
            pressure = r['main']['pressure']
            humidity = r['main']['humidity']
            main = r['weather'][0]['main']
            description = r['weather'][0]['description']
            icon = r['weather'][0]['icon']
            if temp is not None:
                data, _ = CityWeatherData.objects.get_or_create(city=city)
                data.country_code = country_code
                data.coordinate = coordinate
                data.temp = temp
                data.pressure = pressure
                data.humidity = humidity
                data.main = main
                data.description = description
                data.icon = icon
                data.last_updated = timezone.now()
                data.save()


def index(request):
    if not CityWeatherData.objects.exists() or (timezone.now() - CityWeatherData.objects.order_by('-last_updated').first().last_updated).total_seconds() > 60*30:
        update()
    city_data = CityWeatherData.objects.all().order_by('city')
    paginator = Paginator(city_data, 10)
    page = request.GET.get('page')
    city_data = paginator.get_page(page)
    context = {
        'city_data': city_data,
    }
    return render(request, 'main/index.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            message = 'Invalid username or password. Please try again.'
            context = {'message': message}
            return render(request, 'registration/login.html', context)
    else:
        return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    message = 'Successfully logged out.'
    context = {'message' : message}
    return render(request, 'registration/login.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        hashed_password = make_password(password)
        user = User.objects.create(username=username, password=hashed_password)
        user.save()
        return redirect('login')
    else:
        return render(request, 'registration/register.html')
