from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('garage', views.garage_list),
    path('garage/list', views.garage_summary),
    path('garage/<str:pk>', views.garage_detail),
    path('garage', views.garage_list),
    path('user/<str:user_id>/<str:id>', views.user_vehicles),
    path('user/<str:user_id>', views.user),
    path('', RedirectView.as_view(url='static/index.html')),
]