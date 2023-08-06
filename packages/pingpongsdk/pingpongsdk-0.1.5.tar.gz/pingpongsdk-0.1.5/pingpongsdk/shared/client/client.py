import requests


_BASE_URL = "https://mediamagic.dev"


class Client:

    api_key: str = ''


    def __init__(self, api_key: str):
        self._api_key = api_key


    def get(self, path: str):
        try:
            response = requests.get(_BASE_URL + path, headers={
                'Content-Type': 'application/json',
                'x-mediamagic-key': self._api_key,
                'Accept': 'application/json',
            })
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return "A HTTP error occured: %s" % e


    def post(self, path: str, body: dict):
        try:
            response = requests.post(_BASE_URL + path, json=body, headers={
                'Content-Type': 'application/json',
                'x-mediamagic-key': self._api_key,
                'Accept': 'application/json',
            })
            print(response.json())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return "A HTTP error occured: %s" % e
