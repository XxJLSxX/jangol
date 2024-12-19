from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, "home.html")

def forgotpass(request):
    if request.user.is_authenticated:
        return redirect('home') 
    return render(request, "forgotpassword.html")

def signup(request):
    if request.user.is_authenticated:
        return redirect('home') 
    return render(request, "signup.html")

@login_required(login_url='login')
def createprofile(request):
    return render(request, "createform.html")

@login_required(login_url='login')
def viewprofile(request):
    return render(request, "viewprofile.html")

@login_required(login_url='login')
def editprofile(request):
    return render(request, "editprofile.html")

@login_required(login_url='login')
def chat(request):
    return render(request, "chat.html")

#Function
def login_user(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            # Return an 'invalid login' error message.
            messages.error(request, "Invalid login credentials")
            return redirect("login")
    
    return render(request, "login.html", {})

def logout_user(request):
    logout(request)
    return redirect("login")