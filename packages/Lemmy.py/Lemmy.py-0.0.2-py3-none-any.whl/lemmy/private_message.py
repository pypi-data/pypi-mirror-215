import requests
from loguru import logger

from lemmy.auth import Authentication

class PrivateMessage:
    def __init__(self):
        self._auth = Authentication()

    def create(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/private_message", json=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def delete(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/private_message/delete", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def list(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/private_message/list", params=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def mark_as_read(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/private_message/mark_as_read", json=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def report(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/private_message/report", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()