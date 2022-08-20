from django.contrib import admin
from .models import Trains, TrainRoute

# Register your models here.

admin.site.register(Trains)
admin.site.register(TrainRoute)