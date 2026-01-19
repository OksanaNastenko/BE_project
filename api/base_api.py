import requests
from config import BASE_URL, X_API_KEY

class BaseAPI:
    def __init__(self, base_url = BASE_URL, x_api_key = X_API_KEY):
        self.base_url = base_url
        self.x_api_key = x_api_key

    def _url(self, path: str) -> str:
        return f"{self.base_url}{path}"
    
    def _create_headers(self):
        headers = {
            "User-Agent": "BE_project/1.0",
            "Accept": "application/json"
        }

        if self.x_api_key:
            headers["x-api-key"] = self.x_api_key

        return headers

    def request(self, method, path, *, params=None, json=None):
        response = requests.request(
            method=method,
            url=self._url(path),
            params=params,
            json=json,
            headers=self._create_headers(),
            timeout=10,
        )

        response.raise_for_status()

        print("Status:", response.status_code)
        print("URL:", response.url)
        print("Headers:", response.headers.get("Content-Type"))

        try:
            print("Response JSON (parsed):", response.json())
        except ValueError:
            print("Response Text (raw):", response.text)

        return response
