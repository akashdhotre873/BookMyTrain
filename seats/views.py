from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth 
from trains.models import Trains, TrainRoute
from seats.models import Passenger, seat
from wallet.models import wallet
from .models import seat
from django.db.models import Max
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.


def send_email(request, seat_obj, passenger_obj, train_obj):
    coach_no = seat_obj.no // 10 + 1
    to = []
    to.append(passenger_obj.email)
    html_message = render_to_string('mail_base.html', {'source': seat_obj.seat_source, 'destination': seat_obj.seat_destination, "passenger_name":passenger_obj.name, "amount": seat_obj.cost, 'seat_no':seat_obj.no, "coach_no": coach_no, "date": train_obj.date})
    plain_message = strip_tags(html_message)
    send_mail("BookMyRail Ticket", plain_message,"BookMyRail<domain>", to, html_message=html_message, fail_silently=False)








def check_seats(request, train_id, trainroute_source_id, trainroute_destination_id):
    if request.user.is_authenticated==False:
        return redirect('/')
    if request.method=="POST":
        coach_type_selected = request.POST["coach_type"]
        train_obj = Trains.objects.get(pk=train_id)
        FC_coaches = train_obj.FC_coaches
        SC_coaches = train_obj.SC_coaches
        sleeper_coaches = train_obj.sleeper_coaches
        if(sleeper_coaches==0 and coach_type_selected=="sleeper"):
            return HttpResponse("No seats available")
        seat_obj = seat.objects.all().filter(trainid=train_obj.id, coach_type=coach_type_selected).aggregate(Max('no'))
        if(seat_obj["no__max"]==None):
            max_no = 0
        else:
            seat_obj = seat.objects.get(trainid=train_obj.id, coach_type=coach_type_selected, no=seat_obj['no__max'])
            max_no = seat_obj.no
        if coach_type_selected=="FC" and max_no+1>FC_coaches*10:
            return HttpResponse("No seats available in FC class")
        if coach_type_selected=="SC" and max_no+1>SC_coaches*10:
            return HttpResponse("No seats available in SC class")
        if coach_type_selected=="sleeper" and max_no+1>sleeper_coaches*10:
            return HttpResponse("No seats available in sleeper class")

        return redirect("get_details", max_no, train_id, trainroute_source_id, trainroute_destination_id, coach_type_selected)


def get_details(request, max_seat_no, train_id, trainroute_source_id, trainroute_destination_id, coach_type):
    if request.user.is_authenticated==False:
        return redirect('/')
    if request.method=="POST":
        name = request.POST["name"]
        email = request.POST["email"]
        age = request.POST["age"]
        mobile_no = request.POST["mobile_no"]
        gender = request.POST["gender"]

        
        train_obj = Trains.objects.get(pk=train_id)
        seat_obj = seat.objects.all().filter(trainid=train_obj.id, coach_type=coach_type).aggregate(Max('no'))
        if(seat_obj["no__max"]==None):
            max_seat_no = 0
        else:
            seat_obj = seat.objects.get(trainid=train_obj.id, coach_type=coach_type, no=seat_obj['no__max'])
            max_seat_no = seat_obj.no


        # this code is to find cost
        trainroute_source_obj = TrainRoute.objects.get(id=trainroute_source_id)
        trainroute_destination_obj = TrainRoute.objects.get(id=trainroute_destination_id)
        cost = trainroute_destination_obj.cost - trainroute_source_obj.cost
        if coach_type=="FC":
            cost = cost + (cost * 15) // 100
        elif coach_type=="sleeper":
            cost = cost + (cost * 20) // 100
        wallet_obj = wallet.objects.get(user_id=request.user.id)
        if cost > wallet_obj.amount:
            return render(request, "not_enough_money.html")
        else:
            passenger_obj = Passenger(name=name, email=email, age=age, mobile_no=mobile_no, gender=gender)
            passenger_obj.save()
            seat_obj = seat(no=max_seat_no+1, trainid_id=train_id, coach_type=coach_type, seat_source=trainroute_source_obj.route, seat_destination=trainroute_destination_obj.route, booked_by_id=request.user.id, passenger_id_id=passenger_obj.id, cost=cost)
            seat_obj.save()
            wallet_obj.amount = wallet_obj.amount - cost
            wallet_obj.save()
        send_email(request, seat_obj, passenger_obj, train_obj)
        return render(request, "booked.html", {'passenger_obj': passenger_obj, 'seat_obj': seat_obj, 'train_obj': train_obj})
        
    else:
        return render(request, "fill_passenger_details.html")


