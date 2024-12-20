import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, GalleryImage
from django.contrib.auth.hashers import make_password
from datetime import date, datetime
from django.urls import reverse

# Create your views here.
@login_required(login_url='login')
def home(request):
    profiles = Profile.objects.all()
    profile = profiles.first()  # Get the first profile from the QuerySet
    
    if profile:
        birth_date = profile.birthday
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    else:
        birth_date = None
        age = None

    context = {
        'profiles': profiles,
        'birthday': birth_date,
        'age': age
    }
    return render(request, 'home.html', context)

def forgotpass(request):
    if request.user.is_authenticated:
        return redirect('home') 
    return render(request, "forgot_password.html")

@login_required(login_url='login')
def createprofile(request):
    if request.method == "POST":
        user = request.user 
        profile_picture = request.FILES["pet_picture"]
        name = request.POST["petname"]
        original_name, original_ext = os.path.splitext(profile_picture.name)
        new_name = f"{name}{original_ext}"
        profile_picture.name = new_name
        breed = request.POST["petbreed"]
        gender = request.POST["petgender"]
        birthday = request.POST["petbirthday"]
        location = request.POST["location"]
        petprofile = Profile(user=user, profile_picture=profile_picture, name=name, gender=gender, breed=breed, birthday=birthday, location=location) 
        petprofile.save()
        return redirect('home')
    else:
        return render(request, "createform.html")

@login_required(login_url='login')
def viewprofile(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    profile = get_object_or_404(Profile, user=user)
    gallery_images = profile.gallery_images.all()   
    # Calculate age
    today = date.today()
    birth_date = profile.birthday
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    # For Gallery Images
    if request.method == 'POST':
        images = request.FILES.getlist('images')
        if gallery_images.count() + len(images) > 8:
            messages.error(request, "You can only upload up to 8 images.")
            return redirect(reverse('viewprofile', args=[user_id]))
        
        for image in images:
            gallery_image = GalleryImage(profile=profile, image=image)
            gallery_image.save()
        return redirect(reverse('viewprofile', args=[user_id]))
    else:
        form = GalleryImageForm()
    
    return render(request, 'viewprofile.html', {'profile': profile, 'age': age, 'form': form, 'gallery_images': gallery_images})

# Delete Gallery Image
@login_required(login_url='login')
def delete_gallery_image(request, image_id):
    image = get_object_or_404(GalleryImage, id=image_id)
    profile = image.profile

    if request.user != profile.user:
        messages.error(request, "You do not have permission to delete this image.")
        return redirect('viewprofile', user_id=profile.user.id)

    image.delete()
    messages.success(request, "Image deleted successfully.")
    return redirect('viewprofile', user_id=profile.user.id)

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


def signup(request):
    if request.user.is_authenticated:
        return redirect('home') 
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Create and save the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            #messages.success(request, "User registered successfully!")
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("createprofile")
    else:
        form = UserRegistrationForm()
        return render(request, 'signup.html', {'form': form})

# For forgot password
def forgotpass(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST.get("email")

        try:
            # Check if the user exists with the provided email
            user = User.objects.get(email=email)
            # Store user's ID in the session for the reset password step
            request.session['reset_user_id'] = user.id
            return redirect('reset_password')

        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")
            
    return render(request, "forgot_password.html")


def reset_password(request):
    user_id = request.session.get('reset_user_id')

    if not user_id:
        messages.error(request, "Session expired or invalid access.")
        return redirect('forgotpass')

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('reset_password')
        else:
            # Update the user's password
            user = User.objects.get(id=user_id)
            user.password = make_password(password)
            user.save()

            # Clear the session
            del request.session['reset_user_id']

            messages.success(request, "Password reset successful. Please log in.")
            return redirect('login')

    return render(request, "password_reset_confirm.html")

# For Uploading Images in Gallery
class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']

