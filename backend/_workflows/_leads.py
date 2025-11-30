
from _search._mixed_people import search_mixed_people

def get_leads(profile: dict, page: int, page_size: int) -> str:

    titles = profile["titles"]
    locations = profile["locations"]
    
    response = search_mixed_people(titles, locations, page=page, page_size=page_size)
    return response.json()