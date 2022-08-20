from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Trains(models.Model):
    trainno = models.IntegerField()
    Name = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    date = models.DateField()
    FC_coaches = models.IntegerField()
    SC_coaches = models.IntegerField()
    sleeper_coaches = models.IntegerField()


class TrainRoute(models.Model):
    train = models.ForeignKey(Trains, related_name='route', on_delete=models.CASCADE)
    route = models.CharField(max_length=100)
    arrival_date = models.DateField()
    arrival_time = models.TimeField()
    departure_date = models.DateField()
    departure_time = models.TimeField()
    cost = models.IntegerField()



