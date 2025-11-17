"""
Flask application for Travel Agent Assistant API.

This module provides REST API endpoints for:
- Flight search
- Visa requirements checking
- Nearest airport search
- Hotel, car, and activity search
"""
import logging
from flask import Flask, request, jsonify
from amadeus_api import search_flights, get_nearest_airports, search_hotels, search_cars, search_activities, search_location
from sherpa_api import get_visa_requirements

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def hello_world():
    """Root endpoint - returns API status."""
    return jsonify({
        'status': 'active',
        'message': 'Travel Agent Assistant API',
        'version': '1.0.0'
    })

@app.route('/api/flights', methods=['GET'])
def api_search_flights():
    """
    Search for flights between origin and destination.
    
    Query Parameters:
        origin (str): IATA airport code (e.g., 'JFK')
        destination (str): IATA airport code (e.g., 'LHR')
        departure_date (str): Date in YYYY-MM-DD format
        adults (int, optional): Number of adult passengers (default: 1)
    
    Returns:
        JSON: List of flight offers or error message
    """
    try:
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        departure_date = request.args.get('departure_date')
        adults = request.args.get('adults', 1, type=int)

        # Validate required parameters
        if not all([origin, destination, departure_date]):
            logger.warning(f"Missing parameters for flight search: origin={origin}, destination={destination}, date={departure_date}")
            return jsonify({
                'error': 'Missing required parameters',
                'required': ['origin', 'destination', 'departure_date'],
                'optional': ['adults']
            }), 400

        # Validate date format (basic check)
        if len(departure_date) != 10 or departure_date.count('-') != 2:
            logger.warning(f"Invalid date format: {departure_date}")
            return jsonify({
                'error': 'Invalid date format. Use YYYY-MM-DD format'
            }), 400

        logger.info(f"Searching flights: {origin} -> {destination} on {departure_date}")
        flights = search_flights(origin, destination, departure_date, adults)

        if flights:
            logger.info(f"Found {len(flights)} flight options")
            return jsonify(flights)
        else:
            logger.warning(f"No flights found for {origin} -> {destination}")
            return jsonify({
                'error': 'Could not retrieve flight offers',
                'message': 'No flights available for the specified route and date. Try different dates or nearby airports.'
            }), 500
    except Exception as e:
        logger.error(f"Unexpected error in flight search: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

@app.route('/api/nearest-airports', methods=['GET'])
def api_get_nearest_airports():
    """
    Find nearest airports to a given location.
    
    This endpoint first searches for the location by keyword, then finds
    nearby airports. Useful for finding alternative airports for better
    flight options or multi-modal travel suggestions.
    
    Query Parameters:
        keyword (str): Location name (city, airport, etc.)
    
    Returns:
        JSON: List of nearest airports with distances or error message
    """
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            logger.warning("Missing keyword parameter for nearest airports search")
            return jsonify({
                'error': 'Missing required parameter: keyword',
                'message': 'Please provide a location name (e.g., city or airport name)'
            }), 400

        logger.info(f"Searching for location: {keyword}")
        locations = search_location(keyword)
        
        if not locations:
            logger.warning(f"Location not found: {keyword}")
            return jsonify({
                'error': 'Could not find location',
                'message': f'No location found matching "{keyword}". Try a different search term.'
            }), 404

        # Check if location has geographic coordinates
        if not locations[0].get('geoCode'):
            logger.warning(f"Location found but no coordinates: {keyword}")
            return jsonify({
                'error': 'Location found but no coordinates available',
                'message': 'The location was found but geographic coordinates are not available.'
            }), 404

        geo_code = locations[0]['geoCode']
        latitude = geo_code.get('latitude')
        longitude = geo_code.get('longitude')
        
        if not latitude or not longitude:
            logger.warning(f"Invalid coordinates for location: {keyword}")
            return jsonify({
                'error': 'Invalid location coordinates'
            }), 500

        logger.info(f"Finding airports near {latitude}, {longitude}")
        airports = get_nearest_airports(latitude, longitude)

        if airports:
            logger.info(f"Found {len(airports)} nearby airports")
            return jsonify(airports)
        else:
            logger.warning(f"No airports found near {keyword}")
            return jsonify({
                'error': 'Could not retrieve nearest airports',
                'message': 'No airports found near the specified location.'
            }), 500
    except Exception as e:
        logger.error(f"Unexpected error in nearest airports search: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

@app.route('/api/visa-requirements', methods=['GET'])
def api_get_visa_requirements():
    """
    Get visa requirements for travel between countries.
    
    Uses the Sherpa API to determine visa requirements based on:
    - Origin country (where the trip starts)
    - Destination country (where the trip ends)
    - Traveler's nationality
    
    Query Parameters:
        origin (str): ISO country code (e.g., 'US')
        destination (str): ISO country code (e.g., 'FR')
        nationality (str): Traveler's nationality country code (e.g., 'US')
    
    Returns:
        JSON: Visa requirements information or error message
    """
    try:
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        nationality = request.args.get('nationality')

        if not all([origin, destination, nationality]):
            logger.warning(f"Missing parameters for visa check: origin={origin}, destination={destination}, nationality={nationality}")
            return jsonify({
                'error': 'Missing required parameters',
                'required': ['origin', 'destination', 'nationality'],
                'message': 'All three parameters (origin, destination, nationality) are required. Use ISO country codes (e.g., US, FR, GB).'
            }), 400

        # Validate country codes (basic check - should be 2 characters)
        if not all(len(code) == 2 for code in [origin, destination, nationality]):
            logger.warning(f"Invalid country code format: origin={origin}, destination={destination}, nationality={nationality}")
            return jsonify({
                'error': 'Invalid country code format',
                'message': 'Country codes must be 2-letter ISO codes (e.g., US, FR, GB)'
            }), 400

        logger.info(f"Checking visa requirements: {nationality} traveling from {origin} to {destination}")
        visa_info = get_visa_requirements(origin, destination, nationality)

        if visa_info:
            logger.info("Visa requirements retrieved successfully")
            return jsonify(visa_info)
        else:
            logger.warning(f"Could not retrieve visa info for {origin} -> {destination} (nationality: {nationality})")
            return jsonify({
                'error': 'Could not retrieve visa information',
                'message': 'Unable to fetch visa requirements. Please check your API key and try again.'
            }), 500
    except ValueError as e:
        logger.error(f"Configuration error in visa check: {str(e)}")
        return jsonify({
            'error': 'Configuration error',
            'message': 'Sherpa API key is not configured. Please set SHERPA_API_KEY in your environment variables.'
        }), 500
    except Exception as e:
        logger.error(f"Unexpected error in visa requirements check: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

@app.route('/api/hotels', methods=['GET'])
def api_search_hotels():
    """
    Search for hotels in a specific city.
    
    Query Parameters:
        city_code (str): IATA city code (e.g., 'NYC', 'PAR', 'LON')
    
    Returns:
        JSON: List of hotel offers or error message
    """
    try:
        city_code = request.args.get('city_code')
        if not city_code:
            logger.warning("Missing city_code parameter for hotel search")
            return jsonify({
                'error': 'Missing required parameter: city_code',
                'message': 'Please provide an IATA city code (e.g., NYC, PAR, LON)'
            }), 400

        logger.info(f"Searching hotels in city: {city_code}")
        hotels = search_hotels(city_code)
        
        if hotels:
            logger.info(f"Found hotel offers for {city_code}")
            return jsonify(hotels)
        else:
            logger.warning(f"No hotels found for city: {city_code}")
            return jsonify({
                'error': 'Could not retrieve hotel offers',
                'message': f'No hotels found for city code "{city_code}". Try a different city code.'
            }), 500
    except Exception as e:
        logger.error(f"Unexpected error in hotel search: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

@app.route('/api/cars', methods=['GET'])
def api_search_cars():
    city_code = request.args.get('city_code')
    if not city_code:
        return jsonify({'error': 'Missing required parameter: city_code'}), 400
    cars = search_cars(city_code)
    if cars:
        return jsonify(cars)
    else:
        return jsonify({'error': 'Car search not yet available'}), 501

@app.route('/api/activities', methods=['GET'])
def api_search_activities():
    """
    Search for activities near a given location.
    
    First searches for the location by keyword, then finds activities
    near that location's coordinates.
    
    Query Parameters:
        keyword (str): Location name (city, landmark, etc.)
    
    Returns:
        JSON: List of activities or error message
    """
    try:
        keyword = request.args.get('keyword')
        if not keyword:
            logger.warning("Missing keyword parameter for activity search")
            return jsonify({
                'error': 'Missing required parameter: keyword',
                'message': 'Please provide a location name to search for activities'
            }), 400

        logger.info(f"Searching for location: {keyword}")
        locations = search_location(keyword)
        
        if not locations:
            logger.warning(f"Location not found: {keyword}")
            return jsonify({
                'error': 'Could not find location',
                'message': f'No location found matching "{keyword}". Try a different search term.'
            }), 404

        if not locations[0].get('geoCode'):
            logger.warning(f"Location found but no coordinates: {keyword}")
            return jsonify({
                'error': 'Location found but no coordinates available'
            }), 404

        geo_code = locations[0]['geoCode']
        latitude = geo_code.get('latitude')
        longitude = geo_code.get('longitude')
        
        if not latitude or not longitude:
            logger.warning(f"Invalid coordinates for location: {keyword}")
            return jsonify({
                'error': 'Invalid location coordinates'
            }), 500

        logger.info(f"Searching activities near {latitude}, {longitude}")
        activities = search_activities(latitude, longitude)
        
        if activities:
            logger.info(f"Found activities near {keyword}")
            return jsonify(activities)
        else:
            logger.warning(f"No activities found near {keyword}")
            return jsonify({
                'error': 'Could not retrieve activities',
                'message': f'No activities found near "{keyword}". Try a different location.'
            }), 500
    except Exception as e:
        logger.error(f"Unexpected error in activity search: {str(e)}", exc_info=True)
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred. Please try again later.'
        }), 500

if __name__ == '__main__':
    # Run the Flask development server
    # In production, use a proper WSGI server like Gunicorn
    logger.info("Starting Travel Agent Assistant API server")
    app.run(debug=True, host='0.0.0.0', port=5000)
