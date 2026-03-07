"""TrueNAS WebSocket MCP Server."""
from fastmcp import FastMCP

from truenas_ws_mcp.client import TrueNASClient
from truenas_ws_mcp.config import Settings

settings = Settings()
mcp = FastMCP("TrueNAS")

_client: TrueNASClient | None = None


async def get_client() -> TrueNASClient:
    global _client
    if _client is None:
        _client = TrueNASClient(
            url=settings.truenas_url,
            api_key=settings.truenas_api_key,
            verify_ssl=settings.truenas_verify_ssl,
            timeout=settings.truenas_timeout,
        )
        await _client.connect()
    return _client


def main():
    mcp.run()


if __name__ == "__main__":
    main()
