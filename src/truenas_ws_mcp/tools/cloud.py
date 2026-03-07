from truenas_ws_mcp.server import mcp, get_client


@mcp.tool
async def list_cloud_syncs() -> list:
    """List all cloud sync tasks with their status and schedule."""
    client = await get_client()
    return await client.call("cloudsync.query", [])


@mcp.tool
async def run_cloud_sync(task_id: int) -> str:
    """Trigger a cloud sync task to run immediately."""
    client = await get_client()
    await client.call("cloudsync.sync", [task_id])
    return f"Cloud sync task {task_id} triggered."


@mcp.tool
async def list_replications() -> list:
    """List all replication tasks with their status."""
    client = await get_client()
    return await client.call("replication.query", [])


@mcp.tool
async def run_replication(task_id: int) -> str:
    """Trigger a replication task to run immediately."""
    client = await get_client()
    await client.call("replication.run", [task_id])
    return f"Replication task {task_id} triggered."
