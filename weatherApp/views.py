from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect
import requests
from django.shortcuts import render
from django.core.paginator import Paginator
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import cache_page

@cache_page(60*30) 
def index(request):
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'San Francisco', 'Charlotte', 'Indianapolis', 'Seattle', 'Denver', 'Washington', 'Boston', 'Nashville', 'El Paso', 'Detroit', 'Memphis', 'Portland', 'Oklahoma City', 'Las Vegas', 'Louisville', 'Baltimore']
    city_data = []
    for city in cities:
        url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'.format(city, '3ac3c441a33320613634b943eca4199a')
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
            weather_data = {
                'city': city,
                'country_code': country_code,
                'coordinate': coordinate,
                'temp': temp,
                'pressure': pressure,
                'humidity': humidity,
                'main': main,
                'description': description,
                'icon': icon,
            }
            city_data.append(weather_data)
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