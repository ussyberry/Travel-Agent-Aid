"""
Sherpa API integration module.

This module handles interactions with the Sherpa API for visa requirement
information. Sherpa provides comprehensive visa requirement data for
international travel.
"""
import logging
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Sherpa API base URL
SHERPA_API_URL = "https://api.joinsherpa.com/v2"

def get_visa_requirements(origin, destination, nationality):
    """
    Gets visa requirements for a given trip from the Sherpa API.
    
    This function queries the Sherpa API to determine visa requirements
    based on the traveler's nationality, origin country, and destination country.
    
    Args:
        origin (str): ISO country code for origin country (e.g., 'US')
        destination (str): ISO country code for destination country (e.g., 'FR')
        nationality (str): ISO country code for traveler's nationality (e.g., 'US')
    
    Returns:
        dict: Visa requirements information including visa type, requirements,
              and documentation needed, or None if error
    
    Raises:
        ValueError: If SHERPA_API_KEY is not set in environment variables
    
    Note:
        This function requires a valid Sherpa API key. The visa requirements
        feature is optional and the application will work for other features
        without it.
    """
    api_key = os.getenv("SHERPA_API_KEY")
    if not api_key:
        logger.error("SHERPA_API_KEY not found in environment variables")
        raise ValueError("SHERPA_API_KEY must be set in the environment.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Construct payload with country codes (ensure uppercase for ISO codes)
    payload = {
        "trip": {
            "origin": {"countryCode": origin.upper()},
            "destination": {"countryCode": destination.upper()},
            "nationality": {"countryCode": nationality.upper()}
        }
    }

    try:
        logger.info(f"Checking visa requirements: {nationality} -> {destination} (from {origin})")
        response = requests.post(
            f"{SHERPA_API_URL}/trips",
            headers=headers,
            json=payload,
            timeout=10  # 10 second timeout
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        
        visa_data = response.json()
        logger.info("Visa requirements retrieved successfully")
        return visa_data
        
    except requests.exceptions.Timeout:
        logger.error("Sherpa API request timed out")
        return None
    except requests.exceptions.HTTPError as e:
        # Handle HTTP errors (4xx, 5xx)
        status_code = e.response.status_code if e.response else 'N/A'
        logger.error(f"Sherpa API HTTP error {status_code}: {str(e)}")
        
        if status_code == 401:
            logger.error("Invalid or expired Sherpa API key")
        elif status_code == 429:
            logger.warning("Rate limit exceeded for Sherpa API")
        
        return None
    except requests.exceptions.RequestException as e:
        # Handle network errors, connection errors, etc.
        logger.error(f"Error calling Sherpa API: {str(e)}")
        return None
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Unexpected error in visa requirements check: {str(e)}", exc_info=True)
        return None

if __name__ == '__main__':
    # Example usage:
    try:
        # Note: This requires a valid SHERPA_API_KEY in your .env file
        visa_info = get_visa_requirements(origin="US", destination="FR", nationality="US")
        if visa_info:
            print(visa_info)
        else:
            print("Could not retrieve visa information.")
    except ValueError as e:
        print(e)
