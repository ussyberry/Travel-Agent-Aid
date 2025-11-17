from flask import Flask, request, jsonify
from amadeus_api import search_flights, get_nearest_airports, search_hotels, search_cars, search_activities, search_location
from sherpa_api import get_visa_requirements

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/api/flights', methods=['GET'])
def api_search_flights():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    departure_date = request.args.get('departure_date')
    adults = request.args.get('adults', 1)

    if not all([origin, destination, departure_date]):
        return jsonify({'error': 'Missing required parameters'}), 400

    flights = search_flights(origin, destination, departure_date, adults)

    if flights:
        return jsonify(flights)
    else:
        return jsonify({'error': 'Could not retrieve flight offers'}), 500

@app.route('/api/nearest-airports', methods=['GET'])
def api_get_nearest_airports():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Missing required parameter: keyword'}), 400

    locations = search_location(keyword)
    if not locations or not locations[0]['geoCode']:
        return jsonify({'error': 'Could not find location'}), 404

    geo_code = locations[0]['geoCode']
    airports = get_nearest_airports(geo_code['latitude'], geo_code['longitude'])

    if airports:
        return jsonify(airports)
    else:
        return jsonify({'error': 'Could not retrieve nearest airports'}), 500

@app.route('/api/visa-requirements', methods=['GET'])
def api_get_visa_requirements():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    nationality = request.args.get('nationality')

    if not all([origin, destination, nationality]):
        return jsonify({'error': 'Missing required parameters'}), 400

    visa_info = get_visa_requirements(origin, destination, nationality)

    if visa_info:
        return jsonify(visa_info)
    else:
        return jsonify({'error': 'Could not retrieve visa information'}), 500

@app.route('/api/hotels', methods=['GET'])
def api_search_hotels():
    city_code = request.args.get('city_code')
    if not city_code:
        return jsonify({'error': 'Missing required parameter: city_code'}), 400
    hotels = search_hotels(city_code)
    if hotels:
        return jsonify(hotels)
    else:
        return jsonify({'error': 'Could not retrieve hotel offers'}), 500

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
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Missing required parameter: keyword'}), 400

    locations = search_location(keyword)
    if not locations or not locations[0]['geoCode']:
        return jsonify({'error': 'Could not find location'}), 404

    geo_code = locations[0]['geoCode']
    activities = search_activities(geo_code['latitude'], geo_code['longitude'])
    if activities:
        return jsonify(activities)
    else:
        return jsonify({'error': 'Could not retrieve activities'}), 500

if __name__ == '__main__':
    app.run(debug=True)
