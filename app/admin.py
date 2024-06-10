from django.contrib import admin
from .models import City, Address, Lesson, Module, Course, PayType, Payment

admin.site.register([City, Address, Lesson, Module, Course, PayType, Payment])
