from django.urls import path
from . import views


app_name = 'products'


urlpatterns = [
    path('list/', views.ProductListView.as_view(), name="list"),
    path('new/', views.ProductCreateView.as_view(), name="new"),
    path('<int:id>/detail/',
         views.ProductDetailView.as_view(),
         name="details",
         ),
    path('<int:id>/delete/',
         views.ProductDeleteView.as_view(),
         name="delete",
         ),
    path('new-group/',
         views.ProductGroupCreateView.as_view(),
         name="new_group",
         ),
]
