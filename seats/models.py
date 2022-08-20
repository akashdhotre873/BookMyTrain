from django.db import models
from trains.models import Trains
from django.contrib.auth.models import User

# Create your models here.

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile_no = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=1)



class seat(models.Model):
    no = models.IntegerField()
    trainid = models.ForeignKey(Trains, related_name='seat', on_delete=models.CASCADE)
    coach_type = models.CharField(max_length=15)
    seat_source = models.CharField(max_length=100)
    seat_destination = models.CharField(max_length=100)
    booked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_id = models.ForeignKey(Passenger, related_name='passenger', on_delete=models.CASCADE)
    cost = models.IntegerField(default=0)

