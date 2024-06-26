import os
import urllib.parse
from uuid import uuid4

import dotenv
import requests
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

dotenv.load_dotenv()


USER_AGENT = "anthonychu-dynamicsessions-client/0.0.0 (Language=Python)"

class DynamicSessionsClient:
    def __init__(self, pool_management_endpoint, session_id=None):
        self.pool_management_endpoint = pool_management_endpoint
        self.credential = DefaultAzureCredential()
        self.bearer_token_provider = get_bearer_token_provider(self.credential, "https://dynamicsessions.io/.default")
        if session_id is not None:
            self.session_id = session_id
        else:
            self.session_id = str(uuid4())
    
    def _build_url(self, path: str) -> str:
        pool_management_endpoint = self.pool_management_endpoint
        if not pool_management_endpoint:
            raise ValueError("pool_management_endpoint is not set")
        if not pool_management_endpoint.endswith("/"):
            pool_management_endpoint += "/"
        encoded_session_id = urllib.parse.quote(self.session_id)
        query = f"identifier={encoded_session_id}&api-version=2024-02-02-preview"
        query_separator = "&" if "?" in pool_management_endpoint else "?"
        full_url = pool_management_endpoint + path + query_separator + query
        return full_url
        
    def execute(self, python_code: str):
        access_token = self.bearer_token_provider()
        api_url = self._build_url("code/execute")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        }
        body = {
            "properties": {
                "codeInputType": "inline",
                "executionType": "synchronous",
                "code": python_code,
            }
        }

        response = requests.post(api_url, headers=headers, json=body)
        response.raise_for_status()
        response_json = response.json()
        properties = response_json.get("properties", {})
        return properties
    
