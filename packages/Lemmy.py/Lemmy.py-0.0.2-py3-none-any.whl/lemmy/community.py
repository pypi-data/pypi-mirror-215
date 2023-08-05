import requests
from loguru import logger

from lemmy.auth import Authentication

class Community:
    def __init__(self):
        self._auth = Authentication()

    def ban_user(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/ban_user", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def block(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/block", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def create(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/create", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def delete(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/delete", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def follow(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/follow", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def get(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/community", params=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def list(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/community/list", params=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def mod(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/community/mod", json=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def remove(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/remove", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

    def transfer(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/community/transfer", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}