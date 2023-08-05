import requests
from loguru import logger

from lemmy.auth import Authentication

class User:
    def __init__(self):
        self._auth = Authentication()

    def get(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/user", params=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def ban(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/ban", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def block(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/block", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def banned(self, **kwargs) -> dict:

        params = {**kwargs, "auth": self._auth.token}

        re = requests.get(f"{self._auth.api_base_url}/user/banned", params=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def delete_account(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/delete_account", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def get_captcha(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/user/get_captcha", params=params)

        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def leave_admin(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/leave_admin", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def mark_all_as_read(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/mark_all_as_read", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def mention(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/user/mention", params=params)

        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def password_change(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/password_change", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def register(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/register", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()

    def replies(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/user/replies", params=params)

        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def report_count(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/user/report_count", params=params)

        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def save_user_settings(self, **kwargs) -> dict:

        params = kwargs
        params["auth"] = self._auth.token

        re = requests.put(f"{self._auth.api_base_url}/user/save_user_settings", json=params)
        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def unread_count(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.get(f"{self._auth.api_base_url}/user/unread_count", params=params)

        if not re.ok:
            logger.error(f"Error encountered: {re.text}")
            return {}
        return re.json()

    def verify_email(self, **kwargs) -> dict:
        params = {**kwargs, "auth": self._auth.token}
        response = requests.post(f"{self._auth.api_base_url}/user/verify_email", json=params)

        if not response.ok:
            logger.error(f"Error encountered: {response.text}")
            return {}

        return response.json()