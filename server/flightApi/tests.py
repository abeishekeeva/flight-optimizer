from django.test import TestCase
import unittest
from flightOptimizer import FlightOptimizer

# Create your tests here.
class TestRequests(unittest.TestCase):

    def setUp(self):
        self.obj = FlightOptimizer()

    def test_wrong_url(self):
        expected = {
            'error_code': 404,
            'error_type': 'HTTPError'
        }
        obj = FlightOptimizer("https://api.skypicker.com/locat")
        response = obj.get_main_airport_of_city('paris', ['berlin'])
        actual = {
            'error_code': response['error_code'],
            'error_type': response['error_type']
        }
        self.assertEqual(expected, actual)
    
    def test_nonexisting_city(self):
        response = self.obj.get_main_airport_of_city('unicorn_land', ['panda_land'])
        self.assertEqual(response["data"], [None, []])

    def test_correct_data(self):
        response = self.obj.get_main_airport_of_city('paris', ['berlin', 'ibiza'])
        assert len(response["data"]) > 0

    def test_flights_with_no_data(self):
        response = self.obj.get_best_flight_price('Bishek', '')
        assert response["error_message"] == 'No arrival airports are found'

        
        

