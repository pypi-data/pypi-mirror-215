import requests
from loguru import logger

from lemmy.auth import Authentication

class Admin:
    def __init__(self):
        self._auth = Authentication()

    def registration_application_approve(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.put(f"{self._auth.api_base_url}/admin/registration_application/approve", json=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def registration_application_list(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.get(f"{self._auth.api_base_url}/admin/registration_application/list", params=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()