from truenas_ws_mcp.server import mcp, get_client


@mcp.tool
async def system_info() -> dict:
    """Get TrueNAS system information: version, uptime, CPU, RAM, boot time."""
    client = await get_client()
    return await client.call("system.info", [])


@mcp.tool
async def list_alerts() -> list:
    """List all active TrueNAS alerts with severity levels."""
    client = await get_client()
    return await client.call("alert.list", [])


@mcp.tool
async def list_services() -> list:
    """List all services and their running status (SMB, NFS, SSH, etc.)."""
    client = await get_client()
    return await client.call("service.query", [])


@mcp.tool
async def list_jobs() -> list:
    """List recent system jobs with status, progress, and errors."""
    client = await get_client()
    return await client.call("core.get_jobs", [])


@mcp.tool
async def get_audit_log(services: list[str] | None = None, limit: int = 50) -> list:
    """Query audit log entries (auth events, config changes)."""
    client = await get_client()
    filters = []
    if services:
        filters.append(["service", "in", services])
    return await client.call("audit.query", [filters, {"limit": limit}])


@mcp.tool
async def list_cron_jobs() -> list:
    """List all configured cron jobs."""
    client = await get_client()
    return await client.call("cronjob.query", [])


@mcp.tool
async def get_boot_pool() -> dict:
    """Get boot pool health status."""
    client = await get_client()
    return await client.call("boot.get_state", [])
