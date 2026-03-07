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


# Import tool modules so @mcp.tool decorators run
import truenas_ws_mcp.tools.system  # noqa: F401, E402
import truenas_ws_mcp.tools.storage  # noqa: F401, E402
import truenas_ws_mcp.tools.snapshots  # noqa: F401, E402
import truenas_ws_mcp.tools.sharing  # noqa: F401, E402
import truenas_ws_mcp.tools.apps  # noqa: F401, E402
import truenas_ws_mcp.tools.vms  # noqa: F401, E402
import truenas_ws_mcp.tools.network  # noqa: F401, E402
import truenas_ws_mcp.tools.reporting  # noqa: F401, E402
import truenas_ws_mcp.tools.users  # noqa: F401, E402
import truenas_ws_mcp.tools.disks  # noqa: F401, E402
import truenas_ws_mcp.tools.cloud  # noqa: F401, E402
import truenas_ws_mcp.tools.smart  # noqa: F401, E402
import truenas_ws_mcp.tools.updates  # noqa: F401, E402


def main():
    mcp.run()


if __name__ == "__main__":
    main()
