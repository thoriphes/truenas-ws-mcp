"""Integration tests against a live TrueNAS instance.

Run with: TRUENAS_URL=wss://... TRUENAS_API_KEY=... pytest tests/test_integration.py -v
"""
import os

import pytest

TRUENAS_URL = os.environ.get("TRUENAS_URL", "")
TRUENAS_API_KEY = os.environ.get("TRUENAS_API_KEY", "")

pytestmark = [
    pytest.mark.skipif(
        not TRUENAS_URL or not TRUENAS_API_KEY,
        reason="TRUENAS_URL and TRUENAS_API_KEY not set",
    ),
    pytest.mark.asyncio,
]


@pytest.fixture
async def client():
    from truenas_ws_mcp.client import TrueNASClient

    c = TrueNASClient(TRUENAS_URL, TRUENAS_API_KEY, verify_ssl=False, timeout=120.0)
    await c.connect()
    yield c
    await c.close()


async def test_system_info(client):
    result = await client.call("system.info", [])
    assert "version" in result
    assert "uptime" in result


async def test_list_alerts(client):
    result = await client.call("alert.list", [])
    assert isinstance(result, list)


async def test_list_pools(client):
    result = await client.call("pool.query", [])
    assert isinstance(result, list)
    assert len(result) > 0


async def test_get_dataset(client):
    # Filtered query — unfiltered times out on large systems
    result = await client.call("pool.dataset.query", [[["id", "=", "data"]]])
    assert isinstance(result, list)
    assert len(result) > 0


async def test_list_snapshots_filtered(client):
    # Filtered query — unfiltered times out on large systems
    result = await client.call("zfs.snapshot.query", [[["dataset", "=", "data"]]])
    assert isinstance(result, list)


async def test_list_smb_shares(client):
    result = await client.call("sharing.smb.query", [])
    assert isinstance(result, list)


async def test_list_apps(client):
    result = await client.call("app.query", [])
    assert isinstance(result, list)
    assert len(result) > 0


async def test_list_vms(client):
    result = await client.call("vm.query", [])
    assert isinstance(result, list)


async def test_list_interfaces(client):
    result = await client.call("interface.query", [])
    assert isinstance(result, list)
    assert len(result) > 0


async def test_list_users(client):
    result = await client.call("user.query", [])
    assert isinstance(result, list)
    assert len(result) > 0


async def test_list_disks(client):
    result = await client.call("disk.query", [])
    assert isinstance(result, list)
    assert len(result) > 0


async def test_reporting_data(client):
    result = await client.call("reporting.netdata_graph", ["memory", {"unit": "HOUR", "page": 1}])
    assert isinstance(result, list)
    assert len(result) > 0
    assert "data" in result[0]


async def test_list_services(client):
    result = await client.call("service.query", [])
    assert isinstance(result, list)
    assert len(result) > 0
