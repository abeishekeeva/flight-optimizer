import sys 
import argparse
import requests
import json 
from haversine import haversine 
from datetime import date, timedelta 


class FlightOptimizer:

    def __init__(self, location_api=None, flights_api=None):
        self.location_api = location_api or "https://api.skypicker.com/locations"
        self.flights_api = flights_api or "https://api.skypicker.com/aggregation_flights"

    def handle_error(self, err=None, code=None, msg=None, response=None, data=[]):
        
        return {
            "error_type": err.__class__.__name__ if err else None,
            "error_code": code if code else None, 
            "error_message": msg if msg else str(err) if err else None,
            "response": response,
            "data": data
        }
    
    def make_request(self, url, params):
        response = requests.get(url, params=params)
        code = response.status_code
        try:            
            response.raise_for_status()
        except requests.exceptions.ConnectionError as err:
            return self.handle_error(err, code, None, response)
        except requests.exceptions.HTTPError as err:
            return self.handle_error(err, code, None, response)
        except requests.exceptions.Timeout as err:
            return self.handle_error(err, code, None, response)
        except requests.exceptions.RequestException  as err:
            return self.handle_error(err, code, None, response)
    
        return self.handle_error(None, 200, None, response) #if no error just return response with code 200

    def parse_arguments_from_cmd(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--from", help="Departure city")
        parser.add_argument("--to",  nargs='+', help="Destination city")

        try:
            args, unknown = parser.parse_known_args()
            args_dict = vars(args)
            return args_dict
        except Exception as exc:
            raise argparse.ArgumentError("Error with arguments")

    def get_main_airport_of_city(self, departure_city, arrival_cities):
        
        final_response = self.handle_error(None, None, None, None, []) #initialize empty array to store the results

        url = self.location_api
        departure_city_params = {
            "term": departure_city,
            "locale": "en-US",
            "location_types" : 'airport',
            "limit" : 10,
            "active_only" : "true",
            "sort" : "name"
        }
        departure_city_response = self.make_request(url, departure_city_params)
        departure_airport = None
        if departure_city_response["error_message"] is None:                   
            departure_city_response = json.loads(departure_city_response["response"].text)      
            if departure_city_response["locations"]:
                departure_locations = departure_city_response["locations"][0]
                departure_airport = {
                    "id": departure_locations["id"],
                    "city": departure_city,
                    "lat": departure_locations["location"]["lat"],
                    "lon": departure_locations["location"]["lon"]
                }        
        else: 
            return departure_city_response

        final_response["data"].append(departure_airport)
        arrival_airports = [] 
        for city in arrival_cities:
            arrival_city_params = {
                "term": city,
                "locale": "en-US",
                "location_types" : 'airport',
                "limit" : 10,
                "active_only" : "true",
                "sort" : "name"
            }
            
            arrival_city_response = self.make_request(url, arrival_city_params)

            if arrival_city_response["error_message"] is None:
                arrival_city_response = json.loads(arrival_city_response["response"].text)                
                if arrival_city_response["locations"]:
                    arrival_airport = arrival_city_response["locations"][0]
                    city_to = {
                        "id": arrival_airport["id"],
                        "city": city,
                        "lat": arrival_airport["location"]["lat"],
                        "lon": arrival_airport["location"]["lon"]
                    }
                    arrival_airports.append(city_to)                
            else: 
                return arrival_city_response
                
        final_response["data"].append(arrival_airports)
        return final_response

    def get_best_flight_price(self, departure_airport, arrival_airports):
            
        final_response = self.handle_error(None, None, None, None, []) #initialize empty array to store the results

        if departure_airport is None:
            return self.handle_error(None, None, 'No departure airport is found')
            
        if not arrival_airports or arrival_airports is None:
            return self.handle_error(None, None, 'No arrival airports are found')
        
        url = self.flights_api
        
        price_distance_ratio = []    
        for arrival_city in arrival_airports:
            parameters = {
                "fly_from": departure_airport["id"],
                "fly_to": arrival_city["id"],
                "v": 3,
                "date_from": "29/06/2020",#str(date.today().strftime("%d/%m/%Y")),
                "date_to": '27/09/2020',#str((date.today() + timedelta(days=120)).strftime("%d/%m/%Y")),
                "max_fly_duration": 6,
                "flight_type": "oneway",
                "one_for_city": 1,
                "one_per_date": 0,
                "adults": 1,
                "children": 0,
                "infants": 0,
                "partner": "picky",
                "partner_market": "us",
                "curr": "USD" ,
                "locale": "en",
                "limit": 30,
                "sort": "price",
                "asc": 1,
                "xml": 0
            }
            
            distance = round(haversine((departure_airport["lat"], departure_airport["lon"]), (arrival_city["lat"], arrival_city["lon"])),3)
            response = self.make_request(url, parameters) 
        
            if response["error_message"] == None:
                response = json.loads(response["response"].content)
                if response["data"]:
                    price = list(response["data"].values())[0]
                    ratio = round(price/distance, 3)
                    price_distance_ratio.append((arrival_city["city"], ratio, distance, price))
                                
        optimal_flight = None
        
        if price_distance_ratio: 
            optimal_flight = sorted(price_distance_ratio, key=lambda x: x[1])
            final_response["data"] = optimal_flight
        else:
            final_response["error_message"] = 'No flight information for given cities'
        
        return final_response 
                
    def start(self):
        cities = self.parse_arguments_from_cmd() 
        airports_response = self.get_main_airport_of_city(cities["from"], cities["to"])
        if airports_response["data"]:
            departure_airport, arrival_airports = airports_response["data"]
            cheapest_flight = self.get_best_flight_price(departure_airport, arrival_airports)
            if cheapest_flight["data"]:
                city = cheapest_flight["data"][0][0].upper()
                price = cheapest_flight["data"][0][3]
                print("Cheapest flight is to {} at a price of ${}".format(city, price))
            else:
                print(cheapest_flight["error_message"])
        else: 
            print(airports_response)
        

#optimizer = FlightOptimizer()
#optimizer.start()
