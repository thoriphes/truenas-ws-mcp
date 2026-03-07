from truenas_ws_mcp.server import mcp, get_client


@mcp.tool()
async def list_vms() -> list:
    """List all virtual machines with their state, CPU, and RAM configuration."""
    client = await get_client()
    return await client.call("vm.query", [])


@mcp.tool()
async def start_vm(vm_id: int) -> str:
    """Start a virtual machine."""
    client = await get_client()
    await client.call("vm.start", [vm_id])
    return f"VM {vm_id} started successfully."


@mcp.tool()
async def stop_vm(vm_id: int, force: bool = False) -> str:
    """Stop a virtual machine. Attempts graceful shutdown first, forces after timeout.

    RAM/CPU changes require full stop+start from TrueNAS — in-guest reboot does NOT
    re-allocate resources.
    """
    client = await get_client()
    await client.call("vm.stop", [vm_id, {"force": force, "force_after_timeout": True}])
    return f"VM {vm_id} stopped successfully."


@mcp.tool()
async def update_vm(vm_id: int, settings: dict) -> dict:
    """Update VM configuration (RAM, CPUs, etc.).

    Note: RAM/CPU changes only take effect after a full stop+start from TrueNAS —
    rebooting from inside the VM does NOT re-allocate resources.
    """
    client = await get_client()
    return await client.call("vm.update", [vm_id, settings])
