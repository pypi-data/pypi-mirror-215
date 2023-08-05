import requests
from loguru import logger

from lemmy.auth import Authentication

class Search:
    def __init__(self):
        self._auth = Authentication()

    def search(self, **kwargs) -> dict:
            params = {**kwargs, "auth": self._auth.token}
            response = requests.get(f"{self._auth.api_base_url}/search", params=params)

            if not response.ok:
                logger.error(f"Error encountered: {response.text}")
                return {}

            return response.json()