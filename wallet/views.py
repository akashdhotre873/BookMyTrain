from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import wallet
from seats.models import Passenger, seat
from trains.models import Trains
import datetime

# Create your views here.




def add_money(request):
    if request.user.is_authenticated==False:
        return redirect('/')
    
    if request.method=="POST":
        amount = int(request.POST["amount"])
        if amount<1:
            messages.info(request, "Invalid amount")
            return redirect("/wallet")
        if amount>100000:
            messages.info(request, "You can not add more than 1,00,000 Rupees")
            return redirect("/wallet")
        wallet_obj = wallet.objects.get(user_id=request.user.id)
        wallet_obj.amount = wallet_obj.amount + amount
        wallet_obj.save()
        return redirect('/wallet')
        
    else:
        wallet_obj = wallet.objects.get(user_id=request.user.id)
        return render(request, "add_money.html", {'amount':wallet_obj.amount})





def mybookings(request):
    if request.user.is_authenticated==False:
        return redirect('/')
    seat_objs = seat.objects.all().filter(booked_by_id=request.user.id)
    if len(seat_objs)==0:
        return render(request, "no_bookings.html")
    seats = []
    passengers = []
    trains = []
    can_cancel = []
    today_date = datetime.date.today()
    for seat_obj in seat_objs:
        train_obj = Trains.objects.get(pk=seat_obj.trainid_id)
        if(today_date < train_obj.date):
            can_cancel.append(True)
        else:
            can_cancel.append(False)
        passenger_obj = Passenger.objects.get(pk=seat_obj.passenger_id_id)
        seats.append(seat_obj)
        passengers.append(passenger_obj)
        trains.append(train_obj)
       
    everything = zip(seats, passengers, trains, can_cancel)
    return render(request, "mybookings.html", {'everything':everything})





def cancel_ticket(request, id):
    if request.method=="POST":
        seat_obj = seat.objects.get(pk=id)
        cost = seat_obj.cost
        passenger_obj = Passenger.objects.get(pk=seat_obj.passenger_id_id)
        seat_obj.delete()
        passenger_obj.delete()
        wallet_obj = wallet.objects.get(pk=request.user.id)
        wallet_obj.amount = wallet_obj.amount + cost
        wallet_obj.save()
        return redirect("mybookings")