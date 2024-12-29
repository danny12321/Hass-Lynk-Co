import logging
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.components.number import NumberEntity

from .const import COORDINATOR, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]
    vin = entry.data.get("vin")
    async_add_entities(
        [
            LynkCoSensorNumber(
                coordinator,
                vin,
                "Lynk & Co Battery distance",
                "vehicle_record.electricStatus.distanceToEmptyOnBatteryOnly",
                "km",
                None,
                "NumberDeviceClass.DISTANCE"
            ),
        ]
    )


class LynkCoSensorNumber(CoordinatorEntity, NumberEntity):
    def __init__(
        self,
        coordinator,
        vin,
        name,
        data_path,
        unit_of_measurement=None,
        state_mapping=None,
        device_class=None,
        native_value=1.0
    ):
        super().__init__(coordinator)
        self._vin = vin
        self._name = name
        self._data_path = data_path.split(".")
        self._unit_of_measurement = unit_of_measurement
        self._state_mapping = state_mapping
        self.device_class = device_class
        self.native_value = native_value

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"lynk_co_{self._vin}")},
            manufacturer="Lynk & Co",
            name=f"Lynk & Co {self._vin}",
        )

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        data = self.coordinator.data
        for key in self._data_path:
            if data:
                data = data.get(key)
        if self._state_mapping:
            return self._state_mapping.get(data, data)
        return data

    @property
    def available(self):
        if self.coordinator.data:
            data = self.coordinator.data
            for key in self._data_path:
                if data is not None and key in data:
                    data = data[key]
                else:
                    _LOGGER.error(
                        f"Data path not found: {self._data_path}, coodinator.data: {self.coordinator.data}"
                    )
                    return False
            return data != "NO_ENGINE_INFO"
        return False

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement

    @property
    def unique_id(self):
        return f"{self._vin}_{self._name}"

    async def async_set_native_value(self, value: float) -> None:
        """Wouldn't it be nice if you could just charge the car by setting a value?"""
