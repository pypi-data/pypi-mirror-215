import requests
from loguru import logger

from lemmy.auth import Authentication

class Comment:
    def __init__(self):
        self._auth = Authentication()

    def create(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/comment", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def delete(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/comment/delete", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def get(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/comment", params=params)
        if not re.ok:
            logger.error(f"Error encountered while getting community: {re.text}")
            return {}
        return re.json()

    def like(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/comment/like", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def list(self, **kwargs) -> dict:

            params = kwargs
            params["auth"] = self._auth.token

            re = requests.get(f"{self._auth.api_base_url}/comment/list", params=params)
            if not re.ok:
                logger.error(f"Error encountered while getting community: {re.text}")
                return {}
            return re.json()

    def mark_as_read(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/comment/mark_as_read", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

    def remove(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/comment/remove", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

    def report(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/comment/report", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()