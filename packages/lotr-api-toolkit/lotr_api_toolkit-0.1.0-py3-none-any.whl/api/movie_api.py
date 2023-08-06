import requests
class MovieApi:
    BASE_URL = 'https://the-one-api.dev/v2'

    def __init__(self, api_key):
        self.api_key = api_key
    
    def get_all_movies(self):
        response = requests.get(f'{self.BASE_URL}/movie', headers={'Authorization': f'Bearer {self.api_key}'})
        return response.json()

    def get_movie_by_id(self, movie_id):
        response = requests.get(f'{self.BASE_URL}/movie/{movie_id}', headers={'Authorization': f'Bearer {self.api_key}'})
        return response.json()
