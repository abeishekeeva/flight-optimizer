from django.shortcuts import render
from django.http import JsonResponse
import json 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .flightOptimizer import FlightOptimizer
from rest_framework import generics 

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def flight_info(request):
    departure_city = request.GET.get("departure")
    arrival_cities = request.GET.get("arrival").split(',')
    obj = FlightOptimizer()
    airport_response = obj.get_main_airport_of_city(departure_city, arrival_cities)
    dep_airp, arrival_airp = airport_response["data"]
    data = obj.get_best_flight_price(dep_airp, arrival_airp)
    data["Access-Control-Allow-Origin"] = "*"
    return Response(data)