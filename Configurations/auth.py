import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

class Authentication:

    def __init__(self, base_url:str, username:str, password:str):
        self.base_url = base_url
        self.username = username
        self.password = password

    def get_auth_token(self):
        payload = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(f"{self.base_url}/auth", json=payload, headers=headers)
            response.raise_for_status()
            token = response.json().get("token")
            print(f"[auth.py] Token fetched: {token}")
            return token

        except Exception as e:
            print(e)
            return None

# if __name__ == '__main__':
#     auth = Authentication(
#         base_url= os.getenv("BASE_URL"),
#         username = os.getenv("USER_NAME"),
#         password = os.getenv("PASSWORD")
#     )
#
#     token = auth.get_auth_token()
#     print(f"[auth.py] Token fetched: {token}")
