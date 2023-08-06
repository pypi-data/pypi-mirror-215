from __future__ import annotations

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from .event import Event
from .helpers import name_to_key

if TYPE_CHECKING:
    from .command import Command
    from .manager import Manager

_LOGGER = logging.getLogger(__name__)

TRUE_STRINGS = ["true", "enabled", "on", "active", "1"]
FALSE_STRINGS = ["false", "disabled", "off", "inactive", "0"]


def string_to_bool(
    payload_on: str | None, payload_off: str | None, string: str
) -> bool | None:
    """String to bool."""
    if payload_on:
        if string == payload_on:
            return True
        if not payload_off:
            return False

    if payload_off:
        if string == payload_off:
            return False
        if not payload_on:
            return True

    if string.lower() in TRUE_STRINGS:
        return True

    if string.lower() in FALSE_STRINGS:
        return False


class DynamicData:
    """The DynamicData class"""

    def __init__(
        self,
        parent_name: str | None,
        parent_key: str,
        data_id: str,
        data_value_string: str,
        data_name: str | None = None,
    ) -> None:
        name = data_name or data_id
        self.id = data_id
        self.key = f"{parent_key}_{name_to_key(name)}"
        self.name = f"{parent_name} {name}" if parent_name else name
        self.value_string = data_value_string


class Sensor:
    """The Sensor class."""

    value: Any | None = None
    last_known_value: Any | None = None

    def __init__(
        self,
        name: str | None = None,
        key: str | None = None,
        child_id: str | None = None,
        *,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_min: int | float | None = None,
        value_max: int | float | None = None,
        value_renderer: Callable[[str], str] | None = None,
        command_set: Command | None = None,
        command_on: Command | None = None,
        command_off: Command | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        self.name = name
        self.key = key or name_to_key(name)
        self.child_id = child_id
        self.value_type = value_type or str
        self.value_unit = value_unit
        self.value_min = value_min
        self.value_max = value_max
        self.value_renderer = value_renderer
        self.command_set = command_set
        self.command_on = command_on
        self.command_off = command_off
        self.payload_on = payload_on
        self.payload_off = payload_off
        self.options = options or {}
        self.on_update = Event()

    @property
    def is_controllable(self) -> bool:
        if self.value_type == bool and self.command_on and self.command_off:
            return True
        return self.command_set is not None

    def _render(self, value_string: str | None) -> Any | None:
        if value_string is None:
            return None
        if self.value_renderer:
            value_string = self.value_renderer(value_string)
        if self.value_type is bool:
            return string_to_bool(self.payload_on, self.payload_off, value_string)
        if self.value_type is int:
            return int(float(value_string))
        return self.value_type(value_string)

    def _validate(self, value: Any) -> bool:
        if not isinstance(value, self.value_type):
            return False
        if self.value_type == str and (
            (self.value_min and len(value) < self.value_min)
            or (self.value_max and len(value) > self.value_max)
        ):
            return False
        if self.value_type in [int, float] and (
            (self.value_min and value < self.value_min)
            or (self.value_max and value > self.value_max)
        ):
            return False
        return True

    def _update_value(self, data: str | None) -> None:
        try:
            value = self._render(data)
        except Exception as exc:  # pylint: disable=broad-except
            _LOGGER.warning("%s: Render error: %s (%s)", self.key, exc, data)
            value = None

        if self._validate(value):
            self.value = self.last_known_value = value
        else:
            self.value = None

    def update(self, data: str | None) -> None:
        """Update."""
        self._update_value(data)
        self.on_update.notify(self)

    async def async_set(self, manager: Manager, value: Any) -> None:
        """Set."""
        if value == self.value or not self._validate(value):
            return

        if self.value_type == bool and self.command_on and self.command_off:
            command = self.command_on if value else self.command_off
        else:
            command = self.command_set

        await manager.async_execute_command(
            command, context={"id": self.child_id, "value": value}
        )


class DynamicSensor(Sensor):
    """The DynamicSensor class."""

    value: list[Sensor]

    def __init__(
        self,
        name: str | None = None,
        key: str | None = None,
        *,
        separator: str | None = None,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_min: int | float | None = None,
        value_max: int | float | None = None,
        value_renderer: Callable[[str], str] | None = None,
        command_set: Command | None = None,
        command_on: str | None = None,
        command_off: str | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        super().__init__(
            name,
            key,
            value_type=value_type,
            value_unit=value_unit,
            value_min=value_min,
            value_max=value_max,
            value_renderer=value_renderer,
            command_set=command_set,
            command_on=command_on,
            command_off=command_off,
            payload_on=payload_on,
            payload_off=payload_off,
            options=options,
        )
        self.separator = separator
        self.value = []
        self.on_child_added = Event()
        self.on_child_removed = Event()

    @property
    def children_by_key(self) -> dict[str, Sensor]:
        return {child.key: child for child in self.value}

    def _update_value(self, data: list[str] | None) -> None:
        if data is None:
            for child in self.value:
                child.update(None)
            return

        dynamic_data_list = [
            DynamicData(self.name, self.key, *data_items)
            for data_items in [line.split(self.separator, 2) for line in data]
            if len(data_items) >= 2
        ]

        dynamic_data_by_key = {
            dynamic_data.key: dynamic_data for dynamic_data in dynamic_data_list
        }

        for key, dynamic_data in dynamic_data_by_key.items():
            if key not in self.children_by_key:
                self.add_child(dynamic_data)

        for child in self.value:
            if child.key in dynamic_data_by_key:
                dynamic_data = dynamic_data_by_key[child.key]
                child.update(dynamic_data.value_string)
            else:
                self.remove_child(child)

    def add_child(self, dynamic_data: DynamicData) -> None:
        """Add a child."""
        child = Sensor(
            dynamic_data.name,
            dynamic_data.key,
            dynamic_data.id,
            value_type=self.value_type,
            value_unit=self.value_unit,
            value_min=self.value_min,
            value_max=self.value_max,
            value_renderer=self.value_renderer,
            command_set=self.command_set,
            command_on=self.command_on,
            command_off=self.command_off,
            payload_on=self.payload_on,
            payload_off=self.payload_off,
            options=self.options,
        )
        self.value.append(child)
        self.on_child_added.notify(self, child)

    def remove_child(self, child: Sensor) -> None:
        """Remove a child."""
        if child.value is not None:
            child.update(None)
        self.value.remove(child)
        self.on_child_removed.notify(self, child)
