# Part 1 

To see the script itself, see **server/flightApi/flightOptimizer.py**. The file will contain class definition with the following methods: 
2 helper methods: 
```handle_error() ``` returns following response 
``` 
{
  "error_type": errror_type,
  "error_code": error_code, 
  "error_message": error_message,
  "response": response, #returns response object after making request 
  "data": data #if there is no error, any data that needs to be returned will be here 
}
```

```make_request() ``` makes a request with pythons **requests** module and handles exception with the function above. 

```parse_arguments_from_cmd``` will parse the arguments from the command line add values and return dictionary as response. For example:
```
{"from": "bishkek", "to": "almaty,london,paris"}
```
The other 2 main functions that work with the API to retrieve flight information are the following: 

```get_main_airport_of_city(departure_city, arrival_cities)``` that accepts a string as departure_city and an array as arrival_cities. It makes a call to Kiwi's location api 
to retrieve airport codes for the cities that were passed. If no error occurs, then response will be following: 
``` 
{
  "error_type": None,
  "error_code": None, 
  "error_message": None,
  "response": None, 
  "data": [...] #data with the id, latitutde, longitude of airports and cityname 
}
```

```get_best_flight_price(departure_airport, arrival_airports)``` that accepts a string for departure_airport and an array for arrival_airports. The methods makes a call Kiwi's 
flight api to retrieve the flight prices. It also calculates the distance with **haversine** module between departure_airport and each of arrival_airports. 
It returns the same format of response as above where **data** attribute will containe an array sorted ascendingly by price/distance ratio where first element is the cheapest
city to fly to. 


To test the script, 
1. Uncomment two last lines at the bottom of the file
2. Call ```python flightOptimizer --from paris --to berlin, ibiza, barcelona```. Cities after --to must be comma separated.  



# Part 2 
This part includes a minimal interface where a user can input data and see the table with flight information with cheapest flight by price/distance ratio. 
It was built using **Django Restframework** on the backend and **React.js** on the frontend. 
 

To see the interface, go to https://flight-optimizer-react.herokuapp.com/ 

To run this interface locally on your machine, do the following: 
1. Clone the project.
2. Create virtual environment. Go to ```server``` folder and install all python and django dependencies by running ```pip install -r requirements.txt```
3. Go to ```react-client``` folder and install all node.js and react.js dependencies by running ```npm i```
4. Build front-end part with ```npm run build```. 
5. Go to ```server``` folder and run ```python manage.py runserver``` and head to ```http://127.0.0.1:8000/```

Prerequisites for this are: **python**, **node.js**, **npm**

