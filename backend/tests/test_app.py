"""
Unit tests for Flask application endpoints.

These tests verify the API endpoints and request handling.
"""
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


class TestAppEndpoints(unittest.TestCase):
    """Test cases for Flask API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        self.app = app.test_client()
        self.app.testing = True

    def test_root_endpoint(self):
        """Test root endpoint returns API status."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'active')

    def test_flight_search_missing_parameters(self):
        """Test flight search with missing parameters."""
        response = self.app.get('/api/flights')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_flight_search_invalid_date_format(self):
        """Test flight search with invalid date format."""
        response = self.app.get('/api/flights?origin=JFK&destination=LHR&departure_date=2025/06/15')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    @patch('app.search_flights')
    def test_flight_search_success(self, mock_search_flights):
        """Test successful flight search."""
        mock_search_flights.return_value = [
            {
                'price': {'total': '500.00', 'currency': 'USD'},
                'itineraries': [{'segments': []}]
            }
        ]

        response = self.app.get('/api/flights?origin=JFK&destination=LHR&departure_date=2025-06-15&adults=1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    @patch('app.search_flights')
    def test_flight_search_no_results(self, mock_search_flights):
        """Test flight search with no results."""
        mock_search_flights.return_value = None

        response = self.app.get('/api/flights?origin=JFK&destination=LHR&departure_date=2025-06-15')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)

    def test_nearest_airports_missing_keyword(self):
        """Test nearest airports search with missing keyword."""
        response = self.app.get('/api/nearest-airports')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    @patch('app.search_location')
    @patch('app.get_nearest_airports')
    def test_nearest_airports_success(self, mock_get_airports, mock_search_location):
        """Test successful nearest airports search."""
        mock_search_location.return_value = [
            {'geoCode': {'latitude': 48.8566, 'longitude': 2.3522}}
        ]
        mock_get_airports.return_value = [
            {
                'name': 'Paris CDG',
                'iataCode': 'CDG',
                'distance': {'value': 25, 'unit': 'KM'}
            }
        ]

        response = self.app.get('/api/nearest-airports?keyword=Paris')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

    def test_visa_requirements_missing_parameters(self):
        """Test visa requirements with missing parameters."""
        response = self.app.get('/api/visa-requirements')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_visa_requirements_invalid_country_code(self):
        """Test visa requirements with invalid country code format."""
        response = self.app.get('/api/visa-requirements?origin=USA&destination=FR&nationality=US')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    @patch('app.get_visa_requirements')
    def test_visa_requirements_success(self, mock_get_visa):
        """Test successful visa requirements check."""
        mock_get_visa.return_value = {
            'visa': {
                'required': False,
                'type': 'Visa Not Required'
            }
        }

        response = self.app.get('/api/visa-requirements?origin=US&destination=FR&nationality=US')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('visa', data)

    @patch('app.get_visa_requirements')
    def test_visa_requirements_config_error(self, mock_get_visa):
        """Test visa requirements with configuration error."""
        mock_get_visa.side_effect = ValueError("SHERPA_API_KEY must be set")

        response = self.app.get('/api/visa-requirements?origin=US&destination=FR&nationality=US')
        self.assertEqual(response.status_code, 500)
        data = response.get_json()
        self.assertIn('error', data)
        self.assertIn('Configuration error', data['error'])

    def test_hotel_search_missing_city_code(self):
        """Test hotel search with missing city code."""
        response = self.app.get('/api/hotels')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    @patch('app.search_hotels')
    def test_hotel_search_success(self, mock_search_hotels):
        """Test successful hotel search."""
        mock_search_hotels.return_value = [
            {
                'hotel': {'name': 'Test Hotel'},
                'offers': []
            }
        ]

        response = self.app.get('/api/hotels?city_code=NYC')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_activity_search_missing_keyword(self):
        """Test activity search with missing keyword."""
        response = self.app.get('/api/activities')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    @patch('app.search_location')
    @patch('app.search_activities')
    def test_activity_search_success(self, mock_search_activities, mock_search_location):
        """Test successful activity search."""
        mock_search_location.return_value = [
            {'geoCode': {'latitude': 48.8566, 'longitude': 2.3522}}
        ]
        mock_search_activities.return_value = [
            {
                'name': 'Eiffel Tower Tour',
                'shortDescription': 'Guided tour'
            }
        ]

        response = self.app.get('/api/activities?keyword=Paris')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)


if __name__ == '__main__':
    unittest.main()

