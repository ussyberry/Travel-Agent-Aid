"""
Unit tests for Sherpa API integration module.

These tests verify the functionality of the Sherpa API wrapper functions.
Note: Some tests may require valid API credentials or mocking.
"""
import unittest
from unittest.mock import patch, MagicMock
import os
import sys
import requests

# Add parent directory to path to import modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sherpa_api import get_visa_requirements


class TestSherpaAPI(unittest.TestCase):
    """Test cases for Sherpa API functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Mock environment variables
        self.env_patcher = patch.dict(os.environ, {
            'SHERPA_API_KEY': 'test_api_key'
        })
        self.env_patcher.start()

    def tearDown(self):
        """Clean up after tests."""
        self.env_patcher.stop()

    def test_get_visa_requirements_missing_api_key(self):
        """Test that ValueError is raised when API key is missing."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                get_visa_requirements('US', 'FR', 'US')

    @patch('sherpa_api.requests.post')
    def test_get_visa_requirements_success(self, mock_post):
        """Test successful visa requirements retrieval."""
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'visa': {
                'required': False,
                'type': 'Visa Not Required'
            }
        }
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        result = get_visa_requirements('US', 'FR', 'US')
        
        self.assertIsNotNone(result)
        self.assertIn('visa', result)
        mock_post.assert_called_once()
        
        # Verify API call parameters
        call_args = mock_post.call_args
        self.assertIn('headers', call_args.kwargs)
        self.assertIn('json', call_args.kwargs)
        self.assertEqual(call_args.kwargs['headers']['Authorization'], 'Bearer test_api_key')

    @patch('sherpa_api.requests.post')
    def test_get_visa_requirements_http_error(self, mock_post):
        """Test visa requirements with HTTP error."""
        # Mock HTTP error response
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        result = get_visa_requirements('US', 'FR', 'US')
        
        self.assertIsNone(result)

    @patch('sherpa_api.requests.post')
    def test_get_visa_requirements_timeout(self, mock_post):
        """Test visa requirements with timeout error."""
        mock_post.side_effect = requests.exceptions.Timeout()

        result = get_visa_requirements('US', 'FR', 'US')
        
        self.assertIsNone(result)

    @patch('sherpa_api.requests.post')
    def test_get_visa_requirements_country_codes_uppercase(self, mock_post):
        """Test that country codes are converted to uppercase."""
        mock_response = MagicMock()
        mock_response.json.return_value = {'visa': {'required': False}}
        mock_response.raise_for_status = MagicMock()
        mock_post.return_value = mock_response

        get_visa_requirements('us', 'fr', 'us')
        
        # Verify that country codes in payload are uppercase
        call_args = mock_post.call_args
        payload = call_args.kwargs['json']
        self.assertEqual(payload['trip']['origin']['countryCode'], 'US')
        self.assertEqual(payload['trip']['destination']['countryCode'], 'FR')
        self.assertEqual(payload['trip']['nationality']['countryCode'], 'US')


if __name__ == '__main__':
    unittest.main()

