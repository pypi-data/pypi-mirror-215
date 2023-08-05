import requests
from loguru import logger

from lemmy.auth import Authentication

class Site:
    def __init__(self):
        self._auth = Authentication()

    def get(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/site", params=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def edit(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.put(f"{self._auth.api_base_url}/site", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()