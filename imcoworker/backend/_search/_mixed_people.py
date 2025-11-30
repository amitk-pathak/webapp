import requests
from constants import URL_MIXED_PEOPLE_APOLLO, APOLLO_API_KEY
from typing import List

def search_mixed_people(titles: List[str], locations: List[str], email_status: List[str] = ["verified"], page: int = 1, page_size: int = 10):
    # Query parameters
    # For complete list refer https://docs.apollo.io/reference/people-api-search
    
    query_params = {
        "person_titles[]": titles,
        "person_locations[]": locations,
        "page":page,
        "per_page":page_size,
        # "person_seniorities[]": ["Owner", "Director"],
        # "q_keywords": "Sales",
        # "include_similar_titles": True,
        # "organization_locations[]": "US",
        # "q_organization_domains_list[]": "example.com",
        # "contact_email_status[]": email_status
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": APOLLO_API_KEY
    }

    try:
        response = requests.post(URL_MIXED_PEOPLE_APOLLO, params=query_params, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        return response

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    except ValueError as ve:
        print(f"Error parsing JSON: {ve}")
