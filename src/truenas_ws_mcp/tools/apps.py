"""App management tools for TrueNAS."""

from truenas_ws_mcp.server import mcp, get_client


@mcp.tool()
async def list_apps() -> list:
    """List all installed apps with their state."""
    client = await get_client()
    return await client.call("app.query", [])


@mcp.tool()
async def get_app_config(app_name: str) -> dict:
    """Get the full configuration of a specific app."""
    client = await get_client()
    return await client.call("app.config", [app_name])


@mcp.tool()
async def update_app_config(app_name: str, values: dict) -> dict:
    """Update app configuration.

    WARNING: This is a REPLACE operation, not a merge. Any config keys not
    included will revert to defaults. Always get current config first with
    get_app_config, modify the needed values, and send the complete config.
    """
    client = await get_client()
    return await client.call("app.update", [app_name, {"values": values}])


@mcp.tool()
async def install_app(app_name: str, values: dict | None = None) -> dict:
    """Install an app from the catalog."""
    client = await get_client()
    return await client.call("app.create", [{"app_name": app_name, "values": values or {}}])


@mcp.tool()
async def delete_app(app_name: str, confirm: bool = False) -> str:
    """Delete an installed app. Requires confirm=True."""
    if not confirm:
        return "Error: You must pass confirm=True to delete an app. This action is irreversible."
    client = await get_client()
    await client.call("app.delete", [app_name])
    return f"App '{app_name}' has been deleted."


@mcp.tool()
async def start_app(app_name: str) -> str:
    """Start a stopped app."""
    client = await get_client()
    await client.call("app.start", [app_name])
    return f"App '{app_name}' has been started."


@mcp.tool()
async def stop_app(app_name: str) -> str:
    """Stop a running app."""
    client = await get_client()
    await client.call("app.stop", [app_name])
    return f"App '{app_name}' has been stopped."


@mcp.tool()
async def upgrade_app(app_name: str) -> dict:
    """Upgrade an app to the latest available version."""
    client = await get_client()
    return await client.call("app.upgrade", [app_name])


@mcp.tool()
async def redeploy_app(app_name: str) -> str:
    """Redeploy an app with its current configuration."""
    client = await get_client()
    await client.call("app.redeploy", [app_name])
    return f"App '{app_name}' has been redeployed."


@mcp.tool()
async def list_available_apps() -> list:
    """Browse the app catalog for available apps to install."""
    client = await get_client()
    return await client.call("app.available", [])
