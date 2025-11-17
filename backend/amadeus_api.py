"""
Amadeus API integration module.

This module handles all interactions with the Amadeus for Developers API,
including flight search, hotel search, location search, and activity search.
"""
import logging
from amadeus import Client, ResponseError
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

def get_amadeus_client():
    """
    Initializes and returns an Amadeus API client.
    
    Reads credentials from environment variables. Raises ValueError if
    credentials are missing.
    
    Returns:
        Client: Configured Amadeus API client
    
    Raises:
        ValueError: If AMADEUS_CLIENT_ID or AMADEUS_CLIENT_SECRET are not set
    """
    client_id = os.getenv("AMADEUS_CLIENT_ID")
    client_secret = os.getenv("AMADEUS_CLIENT_SECRET")

    if not client_id or not client_secret:
        logger.error("Amadeus API credentials not found in environment variables")
        raise ValueError("AMADEUS_CLIENT_ID and AMADEUS_CLIENT_SECRET must be set in the environment.")

    try:
        client = Client(
            client_id=client_id,
            client_secret=client_secret
        )
        logger.debug("Amadeus API client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Amadeus client: {str(e)}")
        raise

def search_flights(origin, destination, departure_date, adults=1):
    """
    Searches for flights using the Amadeus API.
    
    This function queries the Amadeus Flight Offers Search API to find
    available flights between two airports on a specific date.
    
    Args:
        origin (str): IATA airport code for origin (e.g., 'JFK', 'LHR')
        destination (str): IATA airport code for destination
        departure_date (str): Departure date in YYYY-MM-DD format
        adults (int): Number of adult passengers (default: 1)
    
    Returns:
        list: List of flight offers with pricing and itinerary details, or None if error
    
    Note:
        The Amadeus Test environment has rate limits. For production use,
        upgrade to a paid plan.
    """
    try:
        logger.info(f"Searching flights: {origin} -> {destination} on {departure_date} for {adults} adult(s)")
        amadeus = get_amadeus_client()
        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin.upper(),  # Ensure uppercase for IATA codes
            destinationLocationCode=destination.upper(),
            departureDate=departure_date,
            adults=adults
        )
        
        if response.data:
            logger.info(f"Found {len(response.data)} flight options")
        else:
            logger.warning("No flight offers returned from API")
        
        return response.data
    except ResponseError as error:
        # Handle Amadeus API-specific errors
        logger.error(f"Amadeus API error in flight search: {error.description if hasattr(error, 'description') else str(error)}")
        logger.debug(f"Error code: {error.code if hasattr(error, 'code') else 'N/A'}")
        
        # Check for rate limiting
        if hasattr(error, 'code') and error.code == 429:
            logger.warning("Rate limit exceeded for Amadeus API")
        
        return None
    except ValueError as error:
        # Handle missing credentials
        logger.error(f"Configuration error: {str(error)}")
        return None
    except Exception as error:
        # Handle unexpected errors
        logger.error(f"Unexpected error in flight search: {str(error)}", exc_info=True)
        return None

def get_nearest_airports(latitude, longitude):
    """
    Finds the nearest airports to a given latitude and longitude.
    
    Uses the Amadeus Airport Nearest Relevant API to find airports
    within a reasonable distance of the specified coordinates.
    Useful for finding alternative airports for multi-modal travel suggestions.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        list: List of nearby airports with distances, or None if error
    """
    try:
        logger.info(f"Finding airports near coordinates: {latitude}, {longitude}")
        amadeus = get_amadeus_client()
        response = amadeus.reference_data.locations.airports.get(
            latitude=latitude,
            longitude=longitude
        )
        
        if response.data:
            logger.info(f"Found {len(response.data)} nearby airports")
        else:
            logger.warning("No airports found near specified coordinates")
        
        return response.data
    except ResponseError as error:
        logger.error(f"Amadeus API error in nearest airports search: {error.description if hasattr(error, 'description') else str(error)}")
        return None
    except ValueError as error:
        logger.error(f"Configuration error: {str(error)}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error in nearest airports search: {str(error)}", exc_info=True)
        return None

def search_hotels(city_code):
    """
    Searches for hotels in a given city using the Amadeus Hotel Offers API.
    
    Args:
        city_code (str): IATA city code (e.g., 'NYC', 'PAR', 'LON')
    
    Returns:
        list: List of hotel offers, or None if error
    """
    try:
        logger.info(f"Searching hotels in city: {city_code}")
        amadeus = get_amadeus_client()
        response = amadeus.shopping.hotel_offers.get(cityCode=city_code.upper())
        
        if response.data:
            logger.info(f"Found hotel offers for {city_code}")
        else:
            logger.warning(f"No hotels found for city code: {city_code}")
        
        return response.data
    except ResponseError as error:
        logger.error(f"Amadeus API error in hotel search: {error.description if hasattr(error, 'description') else str(error)}")
        return None
    except ValueError as error:
        logger.error(f"Configuration error: {str(error)}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error in hotel search: {str(error)}", exc_info=True)
        return None

def search_cars(city_code):
    """
    Searches for car rentals in a given city.
    
    Note: This is a placeholder function. Car rental search is not yet
    fully implemented in the Amadeus Python SDK. This function may need
    to be updated when car rental API endpoints become available.
    
    Args:
        city_code (str): IATA city code (e.g., 'NYC', 'PAR', 'LON')
    
    Returns:
        None: Car search is not yet available
    """
    try:
        logger.info(f"Car search requested for city: {city_code}")
        # Note: This is a placeholder for the actual car search API call,
        # as the Amadeus Python SDK might not have a direct method for it.
        # You might need to use the raw `amadeus.get` method with the correct endpoint.
        logger.warning("Car search not yet implemented in the SDK")
        return None
    except (ResponseError, ValueError) as error:
        logger.error(f"Error in car search: {str(error)}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error in car search: {str(error)}", exc_info=True)
        return None

def search_activities(latitude, longitude):
    """
    Searches for activities near a given location using the Amadeus Activities API.
    
    Args:
        latitude (float): Latitude coordinate
        longitude (float): Longitude coordinate
    
    Returns:
        list: List of activities near the location, or None if error
    """
    try:
        logger.info(f"Searching activities near coordinates: {latitude}, {longitude}")
        amadeus = get_amadeus_client()
        response = amadeus.shopping.activities.get(
            latitude=latitude,
            longitude=longitude
        )
        
        if response.data:
            logger.info(f"Found activities near location")
        else:
            logger.warning("No activities found near specified coordinates")
        
        return response.data
    except ResponseError as error:
        logger.error(f"Amadeus API error in activity search: {error.description if hasattr(error, 'description') else str(error)}")
        return None
    except ValueError as error:
        logger.error(f"Configuration error: {str(error)}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error in activity search: {str(error)}", exc_info=True)
        return None

def search_location(keyword):
    """
    Searches for a location (city or airport) and returns its coordinates.
    
    This function is used to find geographic coordinates for a location name,
    which can then be used for finding nearest airports or activities.
    
    Args:
        keyword (str): Location name (city, airport, landmark, etc.)
    
    Returns:
        list: List of matching locations with geographic codes, or None if error
    """
    try:
        logger.info(f"Searching for location: {keyword}")
        amadeus = get_amadeus_client()
        response = amadeus.reference_data.locations.get(
            keyword=keyword,
            subType='CITY,AIRPORT'
        )
        
        if response.data:
            logger.info(f"Found {len(response.data)} location(s) matching '{keyword}'")
        else:
            logger.warning(f"No locations found matching '{keyword}'")
        
        return response.data
    except ResponseError as error:
        logger.error(f"Amadeus API error in location search: {error.description if hasattr(error, 'description') else str(error)}")
        return None
    except ValueError as error:
        logger.error(f"Configuration error: {str(error)}")
        return None
    except Exception as error:
        logger.error(f"Unexpected error in location search: {str(error)}", exc_info=True)
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
