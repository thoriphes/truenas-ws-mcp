"""SMB and NFS sharing management tools."""
from __future__ import annotations

from truenas_ws_mcp.server import get_client, mcp


@mcp.tool()
async def list_smb_shares() -> list:
    """List all SMB shares."""
    client = await get_client()
    return await client.call("sharing.smb.query", [])


@mcp.tool()
async def create_smb_share(
    path: str,
    name: str,
    comment: str | None = None,
    readonly: bool = False,
    browsable: bool = True,
) -> dict:
    """Create a new SMB share. Path must start with /mnt/."""
    if not path.startswith("/mnt/"):
        raise ValueError("Path must start with /mnt/.")
    config: dict = {
        "path": path,
        "name": name,
        "ro": readonly,
        "browsable": browsable,
    }
    if comment is not None:
        config["comment"] = comment
    client = await get_client()
    return await client.call("sharing.smb.create", [config])


@mcp.tool()
async def delete_smb_share(id: int, confirm: bool = False) -> str:
    """Delete an SMB share by ID. Requires confirm=True."""
    if not confirm:
        return "Error: You must pass confirm=True to delete an SMB share. This action is irreversible."
    client = await get_client()
    await client.call("sharing.smb.delete", [id])
    return f"SMB share {id} deleted successfully."


@mcp.tool()
async def list_nfs_exports() -> list:
    """List all NFS exports."""
    client = await get_client()
    return await client.call("sharing.nfs.query", [])


@mcp.tool()
async def create_nfs_export(
    path: str,
    comment: str | None = None,
    readonly: bool = False,
    networks: list[str] | None = None,
    hosts: list[str] | None = None,
) -> dict:
    """Create a new NFS export. Path must start with /mnt/."""
    if not path.startswith("/mnt/"):
        raise ValueError("Path must start with /mnt/.")
    config: dict = {
        "path": path,
        "ro": readonly,
    }
    if comment is not None:
        config["comment"] = comment
    if networks is not None:
        config["networks"] = networks
    if hosts is not None:
        config["hosts"] = hosts
    client = await get_client()
    return await client.call("sharing.nfs.create", [config])


@mcp.tool()
async def delete_nfs_export(id: int, confirm: bool = False) -> str:
    """Delete an NFS export by ID. Requires confirm=True."""
    if not confirm:
        return "Error: You must pass confirm=True to delete an NFS export. This action is irreversible."
    client = await get_client()
    await client.call("sharing.nfs.delete", [id])
    return f"NFS export {id} deleted successfully."
