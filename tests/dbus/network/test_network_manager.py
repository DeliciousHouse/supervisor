"""Test NetworkInterface."""
from unittest.mock import AsyncMock

import pytest

from supervisor.dbus.const import ConnectionStateType
from supervisor.dbus.network import NetworkManager
from supervisor.exceptions import HostNotSupportedError

from tests.const import TEST_INTERFACE
from tests.dbus.network.setting.test_init import SETTINGS_WITH_SIGNATURE

# pylint: disable=protected-access


@pytest.mark.asyncio
async def test_network_manager(network_manager: NetworkManager):
    """Test network manager update."""
    assert TEST_INTERFACE in network_manager.interfaces


@pytest.mark.asyncio
async def test_network_manager_version(network_manager: NetworkManager):
    """Test if version validate work."""
    await network_manager._validate_version()
    assert network_manager.version == "1.22.10"

    network_manager.dbus.get_properties = AsyncMock(return_value={"Version": "1.13.9"})
    with pytest.raises(HostNotSupportedError):
        await network_manager._validate_version()
    assert network_manager.version == "1.13.9"


async def test_check_connectivity(network_manager: NetworkManager, dbus: list[str]):
    """Test connectivity check."""
    dbus.clear()
    assert await network_manager.check_connectivity() == 4
    assert dbus == [
        "/org/freedesktop/NetworkManager-org.freedesktop.NetworkManager.Connectivity"
    ]

    dbus.clear()
    assert await network_manager.check_connectivity(force=True) == 4
    assert dbus == [
        "/org/freedesktop/NetworkManager-org.freedesktop.NetworkManager.CheckConnectivity"
    ]


async def test_activate_connection(network_manager: NetworkManager, dbus: list[str]):
    """Test activate connection."""
    dbus.clear()
    connection = await network_manager.activate_connection(
        "/org/freedesktop/NetworkManager/Settings/1",
        "/org/freedesktop/NetworkManager/Devices/1",
    )
    assert connection.state == ConnectionStateType.ACTIVATED
    assert connection.setting_object == "/org/freedesktop/NetworkManager/Settings/1"
    assert dbus == [
        "/org/freedesktop/NetworkManager-org.freedesktop.NetworkManager.ActivateConnection"
    ]


async def test_add_and_activate_connection(
    network_manager: NetworkManager, dbus: list[str]
):
    """Test add and activate connection."""
    dbus.clear()
    settings, connection = await network_manager.add_and_activate_connection(
        SETTINGS_WITH_SIGNATURE, "/org/freedesktop/NetworkManager/Devices/1"
    )
    assert settings.connection.uuid == "0c23631e-2118-355c-bbb0-8943229cb0d6"
    assert settings.ipv4.method == "auto"
    assert connection.state == ConnectionStateType.ACTIVATED
    assert connection.setting_object == "/org/freedesktop/NetworkManager/Settings/1"
    assert dbus == [
        "/org/freedesktop/NetworkManager-org.freedesktop.NetworkManager.AddAndActivateConnection",
        "/org/freedesktop/NetworkManager/Settings/1-org.freedesktop.NetworkManager.Settings.Connection.GetSettings",
    ]
