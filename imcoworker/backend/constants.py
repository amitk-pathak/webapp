import os

URL_HEALTH_APOLLO = "https://api.apollo.io/v1/auth/health"
URL_MIXED_PEOPLE_APOLLO = "https://api.apollo.io/api/v1/mixed_people/api_search"
APOLLO_API_KEY = os.getenv("APOLLO_API_KEY", "")
OPENAPI_API_KEY = os.getenv("OPENAPI_API_KEY", "")