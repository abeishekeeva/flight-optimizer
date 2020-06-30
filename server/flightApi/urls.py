from django.urls import path
from . import views

urlpatterns = [
    path('api/flights/', views.flight_info, name="flight_info")
]