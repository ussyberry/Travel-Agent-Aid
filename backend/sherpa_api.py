# This file will handle all interactions with the Sherpa API.
import requests
from dotenv import load_dotenv
import os

load_dotenv()

SHERPA_API_URL = "https://api.joinsherpa.com/v2"

def get_visa_requirements(origin, destination, nationality):
    """
    Gets visa requirements for a given trip from the Sherpa API.
    """
    api_key = os.getenv("SHERPA_API_KEY")
    if not api_key:
        raise ValueError("SHERPA_API_KEY must be set in the environment.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "trip": {
            "origin": {"countryCode": origin},
            "destination": {"countryCode": destination},
            "nationality": {"countryCode": nationality}
        }
    }

    try:
        response = requests.post(f"{SHERPA_API_URL}/trips", headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Sherpa API: {e}")
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
