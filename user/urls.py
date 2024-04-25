from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('list/', views.UserListView.as_view(), name='list'),
    path('new/', views.UserCreateView.as_view(), name='new'),
    path('<int:id>/details/', views.UserDetailView.as_view(), name='details'),
    path('<int:id>/delete/', views.UserDeleteView.as_view(), name='delete'),
    path('minha-conta/', views.MyAccountView.as_view(), name='account'),
    path('minha-conta/change-password/',
         views.MyAccountView.as_view(),
         name='change-password',
         ),
]
