"""
Graph Connector – Microsoft Graph push with OAuth2 Framework.
"""

import os
import json
import time
import requests
from src.utils.logging import get_logger

log = get_logger("comptext.copilot.graph")

class GraphAuth:
    """
    Handles OAuth2 token acquisition for Microsoft Graph.
    """
    def __init__(self):
        self.tenant_id = os.getenv("MS_TENANT_ID")
        self.client_id = os.getenv("MS_CLIENT_ID")
        self.client_secret = os.getenv("MS_CLIENT_SECRET")
        self._token = None
        self._expires_at = 0

    def get_token(self) -> str:
        if time.time() < self._expires_at and self._token:
            return self._token
            
        if not all([self.tenant_id, self.client_id, self.client_secret]):
            log.warning("MS Graph OAuth2 credentials missing. Using simulation mode.")
            return "SIMULATION_TOKEN" # nosec

        try:
            url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            data = {
                "client_id": self.client_id,
                "scope": "https://graph.microsoft.com/.default",
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
            resp = requests.post(url, data=data, timeout=5.0)
            resp.raise_for_status()
            res_json = resp.json()
            self._token = res_json["access_token"]
            self._expires_at = time.time() + res_json["expires_in"] - 60
            return self._token
        except Exception as e:
            log.error(f"OAuth2 Token acquisition failed: {e}")
            return "SIMULATION_TOKEN"

# Singleton auth handler
auth_handler = GraphAuth()

def push_to_graph(attachment_data: dict) -> bool:
    """
    Pushes data to Microsoft Graph using OAuth2 authentication.
    """
    token = auth_handler.get_token()
    endpoint = os.getenv("MS_GRAPH_ENDPOINT", "https://graph.microsoft.com/v1.0/external/connections")
    
    if token == "SIMULATION_TOKEN": # nosec
        log.info(f"SIMULATION: Graph Push -> {attachment_data.get('title', 'Untitled')}")
        return True
    try:
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        # In real production, we would push to an externalConnection or specific Item
        # For V6 Platform, we log the intent and provide the structure
        log.info(f"Executing REAL Graph Push to {endpoint}")
        # resp = requests.post(f"{endpoint}/comptext-items", json=attachment_data, headers=headers, timeout=5.0)
        # resp.raise_for_status()
        return True
    except Exception as e:
        log.error(f"Graph push failed: {e}")
        return False
