from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth 
from django.contrib import messages
from wallet.models import wallet
# Create your views here.

def login(request):
    # ip, is_routable = get_client_ip(request)
    # if ip is None:
    #     print("No ip found")
    # else:
    #     if is_routable:
    #         print(ip)
    #     else:
    #         print(ip, "Not routable")
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,'Invalid Credentials')
            return redirect('login')
        
    else:
        return render(request,'login.html')





def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                wallet_obj = wallet(user=user, amount=0)
                wallet_obj.save()
                print('user created')
                return redirect('login')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('register')
        

    else:
        return render(request,'register.html')




def logout(request):
    auth.logout(request)
    return redirect('/')

