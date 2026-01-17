import requests
from config import BASE_URL

class BaseAPI:
    def __init__(self, base_url = BASE_URL):
        self.base_url = base_url

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path}"

    def request(self, method, path, *, params=None, json=None):
        response = requests.request(
            method=method,
            url=self._url(path),
            params=params,
            json=json,
            timeout=10,
        )

        response.raise_for_status()

        return response
