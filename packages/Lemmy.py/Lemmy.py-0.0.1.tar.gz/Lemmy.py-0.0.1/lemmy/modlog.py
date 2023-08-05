import requests
from loguru import logger

from lemmy.auth import Authentication

class Modlog:
    def __init__(self):
        self._auth = Authentication()

    def get(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/modlog", params=params)
        if not re.ok:
            logger.error(f"Error encountered while getting community: {re.text}")
            return {}
        return re.json()