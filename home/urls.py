from django.urls import path
from . import views


app_name = 'home'


urlpatterns = [
    path('', views.LoginView.as_view(), name="login"),
    path('login/', views.LoginView.as_view(), name="authentication"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('home/', views.HomeView.as_view(), name="main"),
]
