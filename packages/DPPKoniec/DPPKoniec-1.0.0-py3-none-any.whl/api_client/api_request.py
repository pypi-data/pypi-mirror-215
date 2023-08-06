import requests


class APIRequest:
    def send_get_request(self, name):
        response = requests.get('https://restcountries.com/v3/name/' + name)
        data = response.json()
        if isinstance(data, list):
            data = data[0]
        return data

