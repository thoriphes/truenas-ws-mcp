from truenas_ws_mcp.server import mcp, get_client


@mcp.tool()
async def list_users() -> list:
    """List all system users."""
    client = await get_client()
    return await client.call("user.query", [])


@mcp.tool()
async def get_user(username: str) -> dict:
    """Get details for a specific user."""
    client = await get_client()
    results = await client.call("user.query", [["username", "=", username]])
    if not results:
        raise ValueError(f"User '{username}' not found")
    return results[0]


@mcp.tool()
async def create_user(
    username: str,
    full_name: str,
    password: str,
    email: str | None = None,
    shell: str = "/usr/bin/bash",
    groups: list[int] | None = None,
) -> dict:
    """Create a new system user."""
    config = {
        "username": username,
        "full_name": full_name,
        "password": password,
        "shell": shell,
    }
    if email is not None:
        config["email"] = email
    if groups is not None:
        config["groups"] = groups

    client = await get_client()
    return await client.call("user.create", [config])


@mcp.tool()
async def update_user(user_id: int, properties: dict) -> dict:
    """Update user properties."""
    client = await get_client()
    return await client.call("user.update", [user_id, properties])


@mcp.tool()
async def delete_user(user_id: int, confirm: bool = False) -> str:
    """Delete a user. Requires confirm=True."""
    if not confirm:
        return "Error: You must set confirm=True to delete a user."
    client = await get_client()
    await client.call("user.delete", [user_id])
    return f"User {user_id} deleted successfully."
