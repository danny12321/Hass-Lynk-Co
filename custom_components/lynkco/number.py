import logging

from custom_components.lynkco.sensors.lynk_co_sensor_number import LynkCoSensorNumber
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
