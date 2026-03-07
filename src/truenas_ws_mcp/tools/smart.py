from truenas_ws_mcp.server import mcp, get_client


@mcp.tool
async def list_smart_results() -> list:
    """List SMART test results for all disks."""
    client = await get_client()
    return await client.call("smart.test.results", [])


@mcp.tool
async def run_smart_test(disks: list[str], test_type: str = "SHORT") -> str:
    """Run a SMART test on specified disks. test_type: SHORT or LONG. Note: TrueNAS 25.10 removed SMART scheduling from the API — these are manual tests only."""
    client = await get_client()
    await client.call("smart.test.manual_test", [disks, test_type])
    return f"SMART {test_type} test started on disks: {', '.join(disks)}"
