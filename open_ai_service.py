import logging
from typing import Optional

import pinecone
import requests
from http import HTTPStatus
from langchain.chains.question_answering import load_qa_chain
from langchain import OpenAI
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings

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
    def open_ai_query(query: str, model: str, gpt_conversation_history: list ) -> str:
        try:
            url = f"{Config.OPEN_AI_SVC_URL}/api/v1/completions"
            token = OpenAIService.get_token()
            headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}
            print(gpt_conversation_history)
            payload = OpenAIService._generate_payload_for_model(query, model, gpt_conversation_history)

            response = requests.request("POST", url, headers=headers, json=payload, timeout=Config.OPEN_AI_TIMEOUT)
            print(response.json())

            if response.status_code != HTTPStatus.OK:
                logging.info("Status code = %s: %s", response.status_code, response.text)
                return "Error retrieving results"

            if model == "gpt-35-turbo" or model == "gpt-4" or model == "gpt-4-32k":
                result = response.json()["choices"]
                return result[0]["message"]["content"]
            elif model == "bloom-7b1" or model == "gptj-full":
                result = response.json()
                return result["text"][0]
            else:
                result = response.json()["choices"]
                for choice in result:
                    return choice["text"]

        except Exception as e:
            logging.exception(e)
            return "Error retrieving results"

    @staticmethod
    def _generate_payload_for_model(query: str, model: str, gpt_conversation_history) -> dict:

        if model == "text-davinci-003":
            return {
                "deployment_id": model,
                "prompt": query,
                "max_tokens": 1000,
                "temperature": 1.0,
                "n": 1
            }
        elif model == "code-davinci-002":
            return {
                "deployment_id": model,
                "prompt": query,
                "max_tokens": 1000,
                "temperature": 0.0,
                "n": 1
            }
        elif model == "alephalpha":
            return {
                "deployment_id": model,
                "prompt": query,
                "maximum_tokens": 1000
            }
        # elif model == "gpt-35-turbo":
        #     return {
        #         "deployment_id": model,
        #         "prompt": f"{query}",
        #         "messages": [query],
        #         "max_tokens": 4000,
        #         "temperature": 1.0,
        #         "n": 1,
        #         "stop": ["<|im_end|>"]
        #     }
        elif model == "gpt-35-turbo" or model == "gpt-4" or model == "gpt-4-32k":
            return {
                "deployment_id": model,
                "messages": gpt_conversation_history,
                "max_tokens":  5000,
                "temperature": 0.7,
                "frequency_penalty": 0,
                "presence_penalty": 0,
                "top_p": 0.95,
                "stop": "null"
            }
        elif model == "bloom":
            return {
                "deployment_id": model,
                "prompt": query,
                "result_length": 100
            }
        elif model == "gptj":
            return {
                "deployment_id": model,
                "prompt": query,
                "result_length": 100
            }
        elif model == "bloom-7b1":
            return {
                "deployment_id": model,
                "text": [
                    query
                ],
                "temperature": 0.7,
                "top_k": 10,
                "top_p": 0.2,
                "max_new_tokens": 50,
                "repetition_penalty": 1.7,
                "do_sample": True,
                "remove_input_from_output": True
            }
        elif model == "gptj-full":
            return {
                "deployment_id": model,
                "text": [
                    query
                ],
                "temperature": 0.2,
                "top_k": 10,
                "top_p": 0.2,
                "max_new_tokens": 50,
                "repetition_penalty": 1.5,
                "do_sample": True,
                "remove_input_from_output": True
            }

        raise Exception(f"Invalid model {model}")

    @staticmethod
    def open_ai_enterprise_query(query: str) -> str:
        try:
            index_name = 'demo-index'

            # initialize connection (get API key at app.pinecone.io)
            pinecone.init(
                api_key="5e6a8cb6-f036-4a23-9b34-c95aec8e317f",
                environment="us-west1-gcp-free"  # find next to API key
            )
            index = pinecone.Index(index_name)

            embeddings = OpenAIEmbeddings(openai_api_key=Config.OPENAI_API_KEY)
            docsearch = Pinecone.from_existing_index(index_name, embeddings)

            llm = OpenAI(temperature=0, openai_api_key=Config.OPENAI_API_KEY)
            chain = load_qa_chain(llm, chain_type="stuff")

            docs = docsearch.similarity_search(query, include_metadata=True)
            return chain.run(input_documents=docs, question=query)

        except Exception as e:
            logging.exception(e)
            return "Error retrieving results"

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
