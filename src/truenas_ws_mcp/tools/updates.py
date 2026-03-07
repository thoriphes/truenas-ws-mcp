from truenas_ws_mcp.server import mcp, get_client


@mcp.tool
async def check_updates() -> dict:
    """Check for available TrueNAS system updates."""
    client = await get_client()
    return await client.call("update.check_available", [])


@mcp.tool
async def list_certificates() -> list:
    """List all SSL/TLS certificates."""
    client = await get_client()
    return await client.call("certificate.query", [])
