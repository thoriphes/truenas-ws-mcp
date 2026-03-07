"""Tests for TrueNAS WebSocket client."""
import os
import pytest
from truenas_ws_mcp.client import TrueNASClient

TRUENAS_URL = os.environ.get("TRUENAS_URL", "")
TRUENAS_API_KEY = os.environ.get("TRUENAS_API_KEY", "")


def test_url_normalization_https():
    client = TrueNASClient("https://truenas.local", "fake-key")
    assert client._url == "wss://truenas.local/websocket"


def test_url_normalization_bare():
    client = TrueNASClient("truenas.local", "fake-key")
    assert client._url == "wss://truenas.local/websocket"


def test_url_normalization_already_wss():
    client = TrueNASClient("wss://truenas.local/websocket", "fake-key")
    assert client._url == "wss://truenas.local/websocket"


def test_url_normalization_http():
    client = TrueNASClient("http://truenas.local", "fake-key")
    assert client._url == "ws://truenas.local/websocket"


@pytest.mark.skipif(not TRUENAS_URL or not TRUENAS_API_KEY, reason="TRUENAS_URL/TRUENAS_API_KEY not set")
@pytest.mark.asyncio
async def test_connect_and_system_info():
    client = TrueNASClient(TRUENAS_URL, TRUENAS_API_KEY, verify_ssl=False)
    await client.connect()
    info = await client.call("system.info", [])
    assert "version" in info
    assert "uptime" in info
    await client.close()
