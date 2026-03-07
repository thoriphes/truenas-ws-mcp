"""Disk information tools for TrueNAS."""

from truenas_ws_mcp.server import mcp, get_client


@mcp.tool()
async def list_disks() -> list:
    """List all disks with model, serial number, size, and pool membership."""
    client = await get_client()
    disks = await client.call("disk.query", [])
    return [
        {
            "name": d.get("name"),
            "model": d.get("model"),
            "serial": d.get("serial"),
            "size": d.get("size"),
            "pool": d.get("pool"),
        }
        for d in disks
    ]


@mcp.tool()
async def get_disk_temps() -> list:
    """Get current temperatures for all disks."""
    client = await get_client()
    disks = await client.call("disk.query", [])

    results = []
    for d in disks:
        disk_name = d.get("name")
        if not disk_name:
            continue
        try:
            graph = await client.call(
                "reporting.netdata_graph",
                [
                    "disktemp",
                    {
                        "unit": "HOUR",
                        "page": 1,
                        "identifier": disk_name,
                    },
                ],
            )
            # Extract the latest temperature reading from the graph data.
            # The response typically contains a "data" list of data points;
            # each point is a list where the first element after the timestamp
            # is the temperature value.
            temp = None
            if isinstance(graph, dict):
                data_points = graph.get("data", [])
                # Walk backwards to find the most recent non-null reading
                for point in reversed(data_points):
                    if isinstance(point, list) and len(point) >= 2 and point[1] is not None:
                        temp = point[1]
                        break
            results.append({"disk": disk_name, "temperature": temp})
        except Exception:
            # Some disks (e.g. NVMe) may not report temps via this method
            results.append({"disk": disk_name, "temperature": None, "error": "unable to retrieve temperature"})

    return results
