from __future__ import annotations

from collections.abc import Callable
import logging
from typing import TYPE_CHECKING, Any

from .event import Event
from .helpers import name_to_key

if TYPE_CHECKING:
    from .command import Command

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
        sensor_name: str,
        sensor_key: str,
        data_value: str,
        data_name: str,
        data_id: str | None = None,
    ) -> None:
        data_key = name_to_key(data_name)
        self.value_string = data_value
        self.child_name = f"{sensor_name} {data_name}"
        self.child_key = f"{sensor_key}_{data_key}"
        self.child_id = data_id or data_key


class Sensor:
    """The Sensor class."""

    value: Any | None = None
    last_known_value: Any | None = None

    def __init__(
        self,
        name: str,
        key: str | None = None,
        child_id: str | None = None,
        *,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_renderer: Callable[[str], str] | None = None,
        switch_on: Command | None = None,
        switch_off: Command | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        options: dict | None = None,
    ) -> None:
        self.name = name
        self.key = key or name_to_key(name)
        self.child_id = child_id
        self.value_type = value_type or str
        self.value_unit = value_unit
        self.value_renderer = value_renderer
        self.switch_on = switch_on
        self.switch_off = switch_off
        self.payload_on = payload_on
        self.payload_off = payload_off
        self.options = options or {}
        self.on_update = Event()

    @property
    def is_switchable(self) -> bool:
        return self.value_type is bool and self.switch_on and self.switch_off

    def set_value(self, data: str | None) -> None:
        """Set value."""
        value_string = data
        value = None

        if data is not None and self.value_renderer:
            try:
                value_string = self.value_renderer(data)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("%s: Value render error: %s (%s)", self.key, exc, data)

        if value_string is not None:
            try:
                if self.value_type is bool:
                    value = string_to_bool(
                        self.payload_on, self.payload_off, value_string
                    )
                elif self.value_type is int:
                    value = int(float(value_string))
                else:
                    value = self.value_type(value_string)
            except Exception as exc:  # pylint: disable=broad-except
                _LOGGER.warning("%s: Value error: %s (%s)", self.key, exc, value_string)

        self.value = value

        if value is not None:
            self.last_known_value = value

        self.on_update.notify(self)


class DynamicSensor(Sensor):
    """The DynamicSensor class."""

    value: list[Sensor]

    def __init__(
        self,
        name: str,
        key: str | None = None,
        *,
        value_type: type | None = None,
        value_unit: str | None = None,
        value_renderer: Callable[[str], str] | None = None,
        switch_on: str | None = None,
        switch_off: str | None = None,
        payload_on: str | None = None,
        payload_off: str | None = None,
        separator: str | None = None,
        options: dict | None = None,
    ) -> None:
        super().__init__(
            name,
            key,
            value_type=value_type,
            value_unit=value_unit,
            value_renderer=value_renderer,
            switch_on=switch_on,
            switch_off=switch_off,
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

    def set_value(self, data: list[str] | None) -> None:
        if data is None:
            for child in self.value:
                child.set_value(None)

            self.on_update.notify(self)
            return

        dynamic_data_list = [
            DynamicData(self.name, self.key, *data_items)
            for data_items in [line.split(self.separator, 2) for line in data]
            if len(data_items) >= 2
        ]

        dynamic_data_by_key = {
            dynamic_data.child_key: dynamic_data for dynamic_data in dynamic_data_list
        }

        for key, dynamic_data in dynamic_data_by_key.items():
            if key not in self.children_by_key:
                self.add_child(dynamic_data)

        for child in self.value:
            if child.key in dynamic_data_by_key:
                dynamic_data = dynamic_data_by_key[child.key]
                child.set_value(dynamic_data.value_string)
            else:
                self.remove_child(child)

        self.on_update.notify(self)

    def add_child(self, dynamic_data: DynamicData) -> None:
        """Add a child."""
        child = Sensor(
            dynamic_data.child_name,
            dynamic_data.child_key,
            dynamic_data.child_id,
            value_type=self.value_type,
            value_unit=self.value_unit,
            value_renderer=self.value_renderer,
            switch_on=self.switch_on,
            switch_off=self.switch_off,
            options=self.options,
        )
        self.value.append(child)
        self.on_child_added.notify(self, child)

    def remove_child(self, child: Sensor) -> None:
        """Remove a child."""
        if child.value is not None:
            child.set_value(None)

        self.value.remove(child)
        self.on_child_removed.notify(self, child)
