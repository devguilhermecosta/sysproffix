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
    path('groups/',
         views.ProductGourpListView.as_view(),
         name="group_list",
         ),
    path('groups/register/',
         views.ProductGroupRegisterView.as_view(),
         name="group_register",
         ),
    path('groups/<int:id>/edit/',
         views.ProductGroupDetailView.as_view(),
         name="group_edit",
         ),
    path('groups/<int:id>/delete/',
         views.ProductGroupDeleteView.as_view(),
         name="group_delete",
         ),
]
