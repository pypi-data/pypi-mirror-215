import requests
from loguru import logger

from lemmy.auth import Authentication

class Post:
    def __init__(self):
        self._auth = Authentication()

    def create(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/post", json=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def delete(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/post/delete", json=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def feature(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/post/feature", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def get(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/post", params=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def like(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/post/like", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def list(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/post/list", params=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def lock(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/post/lock", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

    def mark_as_read(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/post/mark_as_read", json=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def remove(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.post(f"{self._auth.api_base_url}/post/remove", json=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()

    def report(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/post/report", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def site_metadata(self, **kwargs) -> dict:
        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/post/site_metadata", params=params)
        if not re.ok:
            logger.error(f"Error encountered while getting posts: {re.text}")
            return {}
        return re.json()