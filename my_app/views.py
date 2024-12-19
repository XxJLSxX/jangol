from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
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

#Fun Login
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

# Logout
def logout_user(request):
    logout(request)
    return redirect("login")

# User Registration
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

def register_user(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create and save the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            messages.success(request, "User registered successfully!")
            return redirect('home')  # Replace 'home' with your desired redirect page
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})