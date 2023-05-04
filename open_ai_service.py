import logging
from typing import Optional

import requests
from http import HTTPStatus

from config import Config


class OpenAIService:

    @staticmethod
    def get_token() -> Optional[str]:
        try:
            resp = requests.post(url=Config.OPEN_AI_TOKEN_URL,
                                 auth=(Config.OPEN_AI_CLIENT_ID, Config.OPEN_AI_CLIENT_SECRET),
                                 params={"grant_type": "client_credentials"})

            token = resp.json()["access_token"]
            return token

        except Exception as e:
            logging.exception("Exception obtaining Open AI token: %s", e)
            return None

    @staticmethod
    def open_ai_query(query: str) -> list:
        try:
            url = f"{Config.OPEN_AI_SVC_URL}/api/v1/completions"
            token = OpenAIService.get_token()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
            payload = {
                "deployment_id": "text-davinci-003",
 ##               "deployment_id": "text-ada-001",
                "prompt": query,
                "max_tokens": 1024,
                "temperature": 0,
                "n": 1
            }

            response = requests.request("POST", url, headers=headers, json=payload, timeout=Config.OPEN_AI_TIMEOUT)
 #           print(token)
 #           print(headers)
 #           print(payload)
            if response.status_code != HTTPStatus.OK:
                logging.info("Status code = %s: %s", response.status_code, response.text)
                return []

            choices = response.json()["choices"]
            for choice in choices:
                return choice["text"]

        except Exception as e:
            logging.exception(e)
            return []


    @staticmethod
    def open_ai_get_embeddings(query: str) -> list:
        try:
            url = f"{Config.OPEN_AI_SVC_URL}/api/v1/embeddings"
            token = OpenAIService.get_token()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
            payload = {
                "deployment_id": "text-embedding-ada-002-v2",
                "input": query,
            }

            response = requests.request("POST", url, headers=headers, json=payload, timeout=Config.OPEN_AI_TIMEOUT)
            if response.status_code != HTTPStatus.OK:
                logging.info("Status code = %s: %s", response.status_code, response.text)
                return []

            print(response.json())
            return response.json()["data"][0]["embedding"]


        except Exception as e:
            logging.exception(e)
            return []
