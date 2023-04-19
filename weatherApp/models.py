from django.db import models
from django.contrib.auth.hashers import make_password

class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super(User, self).save(*args, **kwargs)


class CityWeatherData(models.Model):
    city = models.CharField(max_length=100, unique=True)
    country_code = models.CharField(max_length=2)
    coordinate = models.CharField(max_length=100)
    temp = models.FloatField(default=0.0) # Add default value
    pressure = models.IntegerField(default=0.0)
    humidity = models.IntegerField(default=0.0)
    main = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=10)
    last_updated = models.DateTimeField(auto_now=True)

