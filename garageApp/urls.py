from django.urls import path
from . import views
from .views import index

urlpatterns = [
    path('garage', views.garage_list),
    path('garage/<str:pk>', views.garage_detail),
    path('garage', views.garage_list),
    path('user/<str:user_id>/<str:id>', views.user_vehicles),
    path('user/<str:user_id>', views.user),
    path('', index),
]