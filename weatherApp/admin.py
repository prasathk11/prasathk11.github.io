from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User

class MyUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password')

admin.site.register(User, MyUserAdmin)
