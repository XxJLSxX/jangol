from django.urls import path
from . import views
# from .views import login_view

urlpatterns = [
    path('', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('signup/', views.signup, name='signup'),

]