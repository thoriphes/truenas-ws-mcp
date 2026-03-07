from truenas_ws_mcp.server import mcp, get_client


@mcp.tool
async def list_interfaces() -> list:
    """List network interfaces with IPs and link state."""
    client = await get_client()
    return await client.call("interface.query", [])


@mcp.tool
async def get_network_config() -> dict:
    """Get network configuration: DNS servers, gateway, hostname."""
    client = await get_client()
    return await client.call("network.configuration", [])
