from django.urls import path
from . import views

urlpatterns = [
    path('garage', views.garage_list),
    path('garage/<str:pk>', views.garage_detail),
    path('garage', views.garage_list),
    path('user/<str:user_id>/<str:id>', views.user_vehicles),
    path('user/<str:user_id>', views.user),
    path('', views.index, name='index'),
]