import requests

class QuoteApi:
    BASE_URL = 'https://the-one-api.dev/v2'

    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_all_quotes(self):
        response = requests.get(f'{self.BASE_URL}/quote', headers={'Authorization': f'Bearer {self.api_key}'})
        return response.json()

    def get_quote_by_id(self, quote_id):
        response = requests.get(f'{self.BASE_URL}/quote/{quote_id}', headers={'Authorization': f'Bearer {self.api_key}'})
        return response.json()

    def get_quotes_for_movie(self, movie_id):
        response = requests.get(f'{self.BASE_URL}/movie/{movie_id}/quote', headers={'Authorization': f'Bearer {self.api_key}'})
        return response.json()
