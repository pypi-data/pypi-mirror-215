import requests


class APIRequest:
    def send_get_request(self, name):
        response = requests.get('https://restcountries.com/v3/name/' + name)
        return response.json()

