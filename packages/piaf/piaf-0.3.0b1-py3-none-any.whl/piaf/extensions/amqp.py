"""This module enables communication between platforms using the AMQP 0.9.1 protocol."""
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import cast

from piaf.ptf import Extension

try:
    import aiormq
    import aiormq.abc
    from yarl import URL
except ImportError as e:
    print("Install extra amqp-mtp to use amqp message transfer protocol.")
    raise e


@dataclass(frozen=True, eq=True)
class AMQPExtensionSettings:
    """
    A set of settings to configure an instance of the :class:`AMQPExtension` type.
    """

    url: str | URL
    cleanup_interval: int = 300


class AMQPExtension(Extension):
    """
    An extension providing a connection to an AMQP 0.9.1 server.
    """

    def __init__(self, settings: AMQPExtensionSettings) -> None:
        """
        Initialize a new instance of :class:`AMQPExtension`.

        :param settings: extension settings used to setup the connection.
        """
        self._settings = settings
        self._connection: aiormq.Connection | None = None
        self._channels: dict[int, aiormq.Channel] = {}
        self._task: None | asyncio.Task = None

    async def on_start(self) -> None:
        """
        Initialize the connection to the AMQP server.
        """
        self._connection = cast(
            aiormq.Connection, await aiormq.connect(URL(self._settings.url))
        )
        self._task = asyncio.create_task(self._cleanup_task())

    async def on_stop(self):
        """
        Close the connection to the AMQP server.
        """
        if self._task is not None:
            self._task.cancel()
        if self._connection is not None:
            for channel in self._channels.values():
                if not channel.is_closed:
                    await channel.close()
            await self._connection.close()

    async def channel(self) -> aiormq.Channel:
        """
        Open a new channel on the current connection.

        :return: the new channel
        """
        if self._connection is None:
            raise ConnectionError("Connection not initialized")
        channel = cast(aiormq.Channel, await self._connection.channel())
        self._channels[channel.number] = channel
        return channel

    async def _cleanup_task(self) -> None:
        for c_id, channel in self._channels.items():
            if channel.is_closed:
                del self._channels[c_id]
        await asyncio.sleep(self._settings.cleanup_interval)
