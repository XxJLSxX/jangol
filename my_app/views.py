from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request, "home.html")

def signup(request):
    return render(request, "signup.html")

# def login_user(request):
#     return render(request, "login.html")

def signup(request):
    return render(request, "signup.html")

#Function
def login_user(request):
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