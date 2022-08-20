from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TrainRoute, Trains
import datetime
from django.http import HttpResponse
# Create your views here.


def search_trains(request, source, destination, coach_type, date):
    source_trains = TrainRoute.objects.all().filter(route__iexact=source, arrival_date=date)
    destination_trains = TrainRoute.objects.all().filter(route__iexact=destination)
    all_trains = []
    all_temp_trains = []
    for s_train in source_trains:
        for d_train in destination_trains:
            if s_train.train_id == d_train.train_id and s_train.id < d_train.id:
                all_temp_trains.append(s_train)

    for trains in all_temp_trains:
        train_obj = Trains.objects.get(pk=trains.train_id)
        if coach_type!='sleeper':
            all_trains.append(train_obj)
        if coach_type=='sleeper' and train_obj.sleeper_coaches>0:
            all_trains.append(train_obj)

    return all_trains


def home(request):
    if request.user.is_authenticated==False:
        return redirect('/')
    if request.method=='POST':
        source = request.POST['source']
        destination = request.POST['destination']
        coach_type = request.POST['coach_type']
        date = request.POST['date']             #date object here is of type string, you need to convert it to date object
        today_date = datetime.date.today()
        date = datetime.datetime.strptime(date, '%Y-%m-%d')
        date = date.date()
        if(date<today_date):
            messages.info(request, "Please enter valid date")
            return redirect("home")

        #print(source, destination, coach_type, date)
        if source == destination:
            messages.info(request, "Enter different source and destination")
            return redirect("home")
        else:
            all_trains  = search_trains(request, source, destination, coach_type, date)
            if len(all_trains)==0:
                messages.info(request, "No trains available")
                return redirect("home")      
            else:
                all_trainroute_source_id = []
                all_trainroute_destination_id = []
                costs = []
                num = 0
                for train in all_trains:

                    trainroute_source_obj = TrainRoute.objects.get(train_id=train.id, route__iexact=source)
                    all_trainroute_source_id.append(trainroute_source_obj)

                    trainroute_destination_obj = TrainRoute.objects.get(train_id=train.id, route__iexact=destination)
                    all_trainroute_destination_id.append(trainroute_destination_obj)
                    
                    cost = trainroute_destination_obj.cost - trainroute_source_obj.cost
                    if coach_type=="FC":
                        cost = cost + (cost * 15) // 100
                    elif coach_type == "sleeper":
                        cost = cost + (cost * 20) // 100
                    costs.append(cost)
                    
                    #print("source obj: ", trainroute_source_obj.route, trainroute_source_obj.arrival_time, trainroute_source_obj.departure_time)
                    #print("destination obj ", trainroute_destination_obj.route, trainroute_destination_obj.arrival_time, trainroute_destination_obj.departure_time)

                everything = zip(all_trains, all_trainroute_source_id, all_trainroute_destination_id, costs)

                return render(request, "show_trains.html", {'everything': everything, 'date':date, 'coach_type': coach_type})        
        

    else:
        return render(request, "home.html")

