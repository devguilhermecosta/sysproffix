from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='list'),
    path('new/', views.UserCreateView.as_view(), name='new'),
]
