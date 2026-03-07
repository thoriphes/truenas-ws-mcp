"""Storage pool and dataset management tools."""
from __future__ import annotations

from truenas_ws_mcp.server import get_client, mcp


@mcp.tool()
async def list_pools() -> list:
    """List all storage pools with health, capacity, and fragmentation."""
    client = await get_client()
    return await client.call("pool.query", [])


@mcp.tool()
async def get_pool_status(pool_name: str) -> dict:
    """Get detailed pool status with VDEV topology and error counts."""
    client = await get_client()
    results = await client.call("pool.query", [[["name", "=", pool_name]]])
    if not results:
        raise ValueError(f"Pool '{pool_name}' not found")
    return results[0]


@mcp.tool()
async def list_datasets(pool: str | None = None) -> list:
    """List all datasets with usage and quota info. Optionally filter by pool."""
    client = await get_client()
    if pool:
        return await client.call("pool.dataset.query", [[["pool", "=", pool]]])
    return await client.call("pool.dataset.query", [])


@mcp.tool()
async def get_dataset(name: str) -> dict:
    """Get detailed info for a specific dataset."""
    client = await get_client()
    results = await client.call("pool.dataset.query", [[["id", "=", name]]])
    if not results:
        raise ValueError(f"Dataset '{name}' not found")
    return results[0]


@mcp.tool()
async def create_dataset(
    name: str,
    type: str = "FILESYSTEM",
    compression: str | None = None,
    quota: int | None = None,
    recordsize: str | None = None,
    comments: str | None = None,
) -> dict:
    """Create a new ZFS dataset."""
    client = await get_client()
    payload: dict = {"name": name, "type": type}
    if compression is not None:
        payload["compression"] = compression
    if quota is not None:
        payload["quota"] = quota
    if recordsize is not None:
        payload["recordsize"] = recordsize
    if comments is not None:
        payload["comments"] = comments
    return await client.call("pool.dataset.create", [payload])


@mcp.tool()
async def update_dataset(name: str, properties: dict) -> dict:
    """Update dataset properties (compression, quota, comments, etc.)."""
    client = await get_client()
    return await client.call("pool.dataset.update", [name, properties])


@mcp.tool()
async def delete_dataset(name: str, confirm: bool = False) -> str:
    """Delete a dataset. Requires confirm=True."""
    if not confirm:
        return "Error: You must pass confirm=True to delete a dataset. This action is irreversible."
    client = await get_client()
    await client.call("pool.dataset.delete", [name])
    return f"Dataset '{name}' deleted successfully."
