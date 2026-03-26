from truenas_ws_mcp.server import mcp, get_client


@mcp.tool()
async def list_graphs() -> list:
    """List available reporting graphs and their identifiers.

    Available graphs include: cpu, cputemp, memory, disk, interface, load,
    uptime, arcsize, disktemp, and more. Some graphs require an identifier
    (disk name for 'disk'/'disktemp', interface name for 'interface').
    """
    client = await get_client()
    return await client.call("reporting.graphs", [])


@mcp.tool()
async def get_reporting_data(
    graph: str,
    unit: str = "HOUR",
    identifier: str | None = None,
) -> list:
    """Get historical reporting data for a graph.

    Units: HOUR (1h), DAY (24h), WEEK, MONTH, YEAR. Some graphs need an
    identifier (e.g., disk name 'sda' for disk graphs, interface name
    'enp5s0' for network graphs). Response format:
    [{name, identifier, data: [[unix_timestamp, value], ...]}].
    Memory/ARC values in bytes, CPU in percentage.
    """
    query = {"unit": unit, "page": 1}
    if identifier is not None:
        query["identifier"] = identifier
    client = await get_client()
    return await client.call("reporting.netdata_graph", [graph, query])
