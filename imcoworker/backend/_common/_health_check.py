import requests
from constants import URL_HEALTH_APOLLO, APOLLO_API_KEY

def check_apollo_health():

    headers = {
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }

    try:
        response = requests.get(URL_HEALTH_APOLLO, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"An error occurred during health check: {e}")