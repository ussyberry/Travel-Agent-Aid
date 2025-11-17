"""
Unit tests for Amadeus API integration module.

These tests verify the functionality of the Amadeus API wrapper functions.
Note: Some tests may require valid API credentials or mocking.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from amadeus_api import (
    get_amadeus_client,
    search_flights,
    get_nearest_airports,
    search_hotels,
    search_location,
    search_activities
)


class TestAmadeusAPI(unittest.TestCase):
    """Test cases for Amadeus API functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'AMADEUS_CLIENT_ID': 'test_client_id',
            'AMADEUS_CLIENT_SECRET': 'test_client_secret'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()

    def test_get_amadeus_client_missing_credentials(self):
        """Test that ValueError is raised when credentials are missing."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                get_amadeus_client()

    @patch('amadeus_api.Client')
    def test_get_amadeus_client_success(self, mock_client_class):
        """Test successful Amadeus client initialization."""
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        
        client = get_amadeus_client()
        
        self.assertIsNotNone(client)
        mock_client_class.assert_called_once_with(
            client_id='test_client_id',
            client_secret='test_client_secret'
        )

    @patch('amadeus_api.get_amadeus_client')
    def test_search_flights_success(self, mock_get_client):
        """Test successful flight search."""
        # Mock the Amadeus client and response
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                'price': {'total': '500.00', 'currency': 'USD'},
                'itineraries': [{'segments': [{'carrierCode': 'AA'}]}]
            }
        ]
        mock_client.shopping.flight_offers_search.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = search_flights('JFK', 'LHR', '2025-06-15', 1)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        mock_client.shopping.flight_offers_search.get.assert_called_once()

    @patch('amadeus_api.get_amadeus_client')
    def test_search_flights_api_error(self, mock_get_client):
        """Test flight search with API error."""
        from amadeus import ResponseError
        
        mock_client = MagicMock()
        mock_error = ResponseError(response=MagicMock())
        mock_client.shopping.flight_offers_search.get.side_effect = mock_error
        mock_get_client.return_value = mock_client

        result = search_flights('JFK', 'LHR', '2025-06-15', 1)
        
        self.assertIsNone(result)

    @patch('amadeus_api.get_amadeus_client')
    def test_search_location_success(self, mock_get_client):
        """Test successful location search."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                'name': 'Paris',
                'geoCode': {'latitude': 48.8566, 'longitude': 2.3522}
            }
        ]
        mock_client.reference_data.locations.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = search_location('Paris')
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], 'Paris')

    @patch('amadeus_api.get_amadeus_client')
    def test_get_nearest_airports_success(self, mock_get_client):
        """Test successful nearest airports search."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                'name': 'Paris Charles de Gaulle Airport',
                'iataCode': 'CDG',
                'distance': {'value': 25, 'unit': 'KM'}
            }
        ]
        mock_client.reference_data.locations.airports.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = get_nearest_airports(48.8566, 2.3522)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['iataCode'], 'CDG')

    @patch('amadeus_api.get_amadeus_client')
    def test_search_hotels_success(self, mock_get_client):
        """Test successful hotel search."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                'hotel': {'name': 'Test Hotel'},
                'offers': [{'price': {'total': '100.00'}}]
            }
        ]
        mock_client.shopping.hotel_offers.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = search_hotels('NYC')
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)

    @patch('amadeus_api.get_amadeus_client')
    def test_search_activities_success(self, mock_get_client):
        """Test successful activity search."""
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.data = [
            {
                'name': 'Eiffel Tower Tour',
                'shortDescription': 'Guided tour'
            }
        ]
        mock_client.shopping.activities.get.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = search_activities(48.8566, 2.3522)
        
        self.assertIsNotNone(result)
        self.assertEqual(len(result), 1)


if __name__ == '__main__':
    unittest.main()

