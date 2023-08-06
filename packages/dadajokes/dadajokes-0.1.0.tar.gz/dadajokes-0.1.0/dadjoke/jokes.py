import requests


class JokesDb:

    def __init__(self):
        self.url = "https://icanhazdadjoke.com"
        self.headers = {"Accept": "application/json"}

    def get_random_joke(self):
        response = requests.get(self.url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data


    def get_specific_jon(self, id):
        response = requests.get(f"{self.url}/j/{id}", headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data