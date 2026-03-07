from truenas_ws_mcp.server import mcp, get_client


@mcp.tool
async def list_snapshots(dataset: str | None = None) -> list:
    """List ZFS snapshots, optionally filtered by dataset."""
    client = await get_client()
    filters = [["dataset", "=", dataset]] if dataset else []
    return await client.call("zfs.snapshot.query", [filters])


@mcp.tool
async def create_snapshot(dataset: str, name: str, recursive: bool = False) -> dict:
    """Create a manual ZFS snapshot."""
    client = await get_client()
    return await client.call(
        "zfs.snapshot.create",
        [{"dataset": dataset, "name": name, "recursive": recursive}],
    )


@mcp.tool
async def delete_snapshot(snapshot_name: str, confirm: bool = False) -> str:
    """Delete a snapshot. Requires confirm=True. Snapshot format: dataset@name."""
    if not confirm:
        return "Error: confirm must be True to delete a snapshot."
    client = await get_client()
    await client.call("zfs.snapshot.delete", [snapshot_name])
    return f"Snapshot '{snapshot_name}' deleted."


@mcp.tool
async def rollback_snapshot(snapshot_name: str, confirm: bool = False) -> str:
    """Rollback dataset to snapshot. Requires confirm=True. WARNING: destroys newer data."""
    if not confirm:
        return "Error: confirm must be True to rollback a snapshot."
    client = await get_client()
    await client.call("zfs.snapshot.rollback", [snapshot_name])
    return f"Rolled back to snapshot '{snapshot_name}'."


@mcp.tool
async def clone_snapshot(snapshot_name: str, target_dataset: str) -> dict:
    """Clone a snapshot to a new dataset."""
    client = await get_client()
    return await client.call(
        "zfs.snapshot.clone",
        [{"snapshot": snapshot_name, "dataset_dst": target_dataset}],
    )


@mcp.tool
async def list_snapshot_tasks() -> list:
    """List automated snapshot task schedules."""
    client = await get_client()
    return await client.call("pool.snapshottask.query", [])
