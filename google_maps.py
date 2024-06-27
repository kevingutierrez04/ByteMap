import googlemaps
from dotenv import load_dotenv
import os

# need to call Google Maps API and see the values it returns

load_dotenv()
GMAPS_K = os.environ.get('GMAPS_KEY')
gmaps = googlemaps.Client(key=GMAPS_K)


def get_recs(zip, query):  # def get_recs(query, zip):
    try:
        geocode_result = gmaps.geocode(zip)[0]['geometry']['location']
        # querie = "Spicy vegetarian food"
        '''
        url = 'https://places.googleapis.com/v1/places:\f{query}'
        '''
        response = gmaps.places_nearby(
            location=geocode_result, 
            radius='16093', 
            keyword=query, 
            open_now=True
            )
        '''
        recs = {}

        for r in response['results']:  # if needed
            # potential fields of interest:
            recs[r['name']] =
            (r['formatted_address'],
                r['rating'],
                r.get('price_level',
                'Unknown')
            )

        return recs
        '''

        return response

    except googlemaps.exceptions.ApiError as e:
        print(f"Google Maps API Error occurred: {e}")


#print(get_recs('10027'))
