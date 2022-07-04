from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = authenticate(request, username=username, password=password)

            if user is None:
                messages.error(request, "User credentials do not match.")
                return redirect('login')
            elif user and not user.is_active:
                messages.error(request, "User account is either blocked or has expired. Contact administration for assistance!")
                return redirect('login')
            else:
                
                login(request, user)
                return redirect('homepage')
        except User.DoesNotExist:
            messages.error(request, "User account does not exist.")
            return redirect('login')

    return render(request, 'login.html')


@login_required(login_url='login')
def home_page(request):

    context = {
        'object_list': User.objects.all(),
    }

    return render(request, 'homepage.html', context)


@login_required(login_url='login')
def logout_user(request):
    
    logout(request)
    return redirect('login')
    
