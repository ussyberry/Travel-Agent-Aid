# This file will handle all interactions with the Amadeus API.
from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os

load_dotenv()

def get_amadeus_client():
    """
    Initializes and returns an Amadeus API client.
    """
    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET must be set in the environment.")

    return Client(
        client_id=client_id,
        client_secret=client_secret
    )

def search_flights(origin, destination, departure_date, adults=1):
    """
    Searches for flights using the Amadeus API.
    """
    try:
        amadeus = get_amadeus_client()
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destination,
            departureDate=departure_date,
            adults=adults
        )
        return response.data
    except (ResponseError, ValueError) as error:
        print(error)
        return None

def get_nearest_airports(latitude, longitude):
    """
    Finds the nearest airports to a given latitude and longitude.
    """
    try:
        amadeus = get_amadeus_client()
        response = amadeus.reference_data.locations.airports.get(
            latitude=latitude,
            longitude=longitude
        )
        return response.data
    except (ResponseError, ValueError) as error:
        print(error)
        return None

def search_hotels(city_code):
    """
    Searches for hotels in a given city.
    """
    try:
        amadeus = get_amadeus_client()
        response = amadeus.shopping.hotel_offers.get(cityCode=city_code)
        return response.data
    except (ResponseError, ValueError) as error:
        print(error)
        return None

def search_cars(city_code):
    """
    Searches for cars in a given city.
    """
    try:
        amadeus = get_amadeus_client()
        # Note: This is a placeholder for the actual car search API call,
        # as the Amadeus Python SDK might not have a direct method for it.
        # You might need to use the raw `amadeus.get` method with the correct endpoint.
        print("Car search not yet implemented in the SDK.")
        return None
    except (ResponseError, ValueError) as error:
        print(error)
        return None

def search_activities(latitude, longitude):
    """
    Searches for activities near a given location.
    """
    try:
        amadeus = get_amadeus_client()
        response = amadeus.shopping.activities.get(
            latitude=latitude,
            longitude=longitude
        )
        return response.data
    except (ResponseError, ValueError) as error:
        print(error)
        return None

def search_location(keyword):
    """
    Searches for a location (city or airport) and returns its coordinates.
    """
    try:
        amadeus = get_amadeus_client()
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType='CITY,AIRPORT'
        )
        return response.data
    except (ResponseError, ValueError) as error:
        print(error)
        return None

if __name__ == '__main__':
    # Example usage:
    try:
        # ... (previous examples)

        # Example for hotels
        hotels = search_hotels(city_code='BCN')
        if hotels:
            print(hotels)

        # Example for activities
        activities = search_activities(latitude=41.397158, longitude=2.160873)
        if activities:
            print(activities)
    except (ResponseError, ValueError) as error:
        print(error)
