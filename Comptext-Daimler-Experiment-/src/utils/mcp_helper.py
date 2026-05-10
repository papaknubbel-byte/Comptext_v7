"""
MCP Helper – Utilities for interacting with CompText MCP Servers.
"""

import os
import requests
from src.utils.logging import get_logger

log = get_logger("comptext.utils.mcp")

class MCPBridge:
    """
    Bridge to external CompText MCP servers.
    """
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("COMPTEXT_MCP_URL", "http://localhost:3000")
        
    def check_health(self) -> bool:
        try:
            resp = requests.get(f"{self.base_url}/health", timeout=2.0)
            return resp.status_code == 200
        except Exception:
            return False

    def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """
        Calls an MCP tool via the HTTP bridge (if available).
        """
        try:
            resp = requests.post(
                f"{self.base_url}/tools/{tool_name}",
                json=arguments,
                timeout=5.0
            )
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            log.error(f"MCP tool call failed: {tool_name}", extra={"error": str(e)})
            return {"error": str(e), "success": False}

# Singleton instance
mcp_bridge = MCPBridge()
