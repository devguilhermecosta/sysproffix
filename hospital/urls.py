from django.urls import path
from . import views


app_name = 'hospital'

urlpatterns = [
    path('list/', views.HospitalListView.as_view(), name='list'),
    path('new/', views.HospitalRegisterView.as_view(), name='new'),
    path('create/', views.HospitalRegisterView.as_view(), name='create'),
    path('<int:id>/details/', views.HospitalDetailsView.as_view(), name='details'),  # noqa: E501
    path('<int:id>/delete/', views.HospitalDeleteView.as_view(), name='delete'),  # noqa: E501
]
