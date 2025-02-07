"""Connection object for Network Manager."""

from dbus_next.aio.message_bus import MessageBus

from ...utils.dbus import DBus
from ..const import (
    DBUS_ATTR_FREQUENCY,
    DBUS_ATTR_HWADDRESS,
    DBUS_ATTR_MODE,
    DBUS_ATTR_SSID,
    DBUS_ATTR_STRENGTH,
    DBUS_IFACE_ACCESSPOINT,
    DBUS_NAME_NM,
)
from ..interface import DBusInterfaceProxy, dbus_property


class NetworkWirelessAP(DBusInterfaceProxy):
    """NetworkWireless AP object for Network Manager.

    https://developer.gnome.org/NetworkManager/stable/gdbus-org.freedesktop.NetworkManager.AccessPoint.html
    """

    def __init__(self, object_path: str) -> None:
        """Initialize NetworkWireless AP object."""
        self.object_path = object_path
        self.properties = {}

    @property
    @dbus_property
    def ssid(self) -> str:
        """Return details about ssid."""
        return bytes(self.properties[DBUS_ATTR_SSID]).decode()

    @property
    @dbus_property
    def frequency(self) -> int:
        """Return details about frequency."""
        return self.properties[DBUS_ATTR_FREQUENCY]

    @property
    @dbus_property
    def mac(self) -> str:
        """Return details about mac address."""
        return self.properties[DBUS_ATTR_HWADDRESS]

    @property
    @dbus_property
    def mode(self) -> int:
        """Return details about mac address."""
        return self.properties[DBUS_ATTR_MODE]

    @property
    @dbus_property
    def strength(self) -> int:
        """Return details about mac address."""
        return int(self.properties[DBUS_ATTR_STRENGTH])

    async def connect(self, bus: MessageBus) -> None:
        """Get connection information."""
        self.dbus = await DBus.connect(bus, DBUS_NAME_NM, self.object_path)
        self.properties = await self.dbus.get_properties(DBUS_IFACE_ACCESSPOINT)
