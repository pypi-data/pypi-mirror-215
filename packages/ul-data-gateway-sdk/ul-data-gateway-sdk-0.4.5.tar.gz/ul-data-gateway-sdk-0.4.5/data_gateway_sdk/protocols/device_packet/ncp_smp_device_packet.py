from datetime import datetime, tzinfo
from typing import Any, List

from data_aggregator_sdk.integration_message import IntegrationV0MessageData, IntegrationV0MessageCurrentBatteryLevel, IntegrationV0MessageCurrentTemperature, \
    IntegrationV0MessageConsumption, CounterType, ResourceType
from pyncp import decode_data as ncp_decode_data  # type: ignore
from pysmp import decode_getset as smp_getset  # type: ignore


from data_gateway_sdk.errors import DataGatewayDeviceProtocolParsingError
from data_gateway_sdk.protocols.device_packet.device_packet import DevicePacket
from data_gateway_sdk.protocols.device_packet.smp_device_packet import SmpDaily


class NcpSmpV0DevicePacket(DevicePacket):
    mac: int
    packet: SmpDaily

    @classmethod
    def parse(cls, payload: bytes, **kwargs: Any) -> List['NcpSmpV0DevicePacket']:
        try:
            mac_device, smp_data = ncp_decode_data(data=payload)
            return [NcpSmpV0DevicePacket(
                mac=mac_device,
                packet=SmpDaily(
                    **{cmd.name.replace('SMP_', '').lower(): (val.value.isoformat() if isinstance(val.value, datetime) else val.value) for cmd, val in smp_getset(smp_data)},
                ),
            )]
        except Exception as e:  # noqa: B902
            raise DataGatewayDeviceProtocolParsingError('invalid payload', e)

    def to_integration_data(self, received_at: datetime, device_tz: tzinfo, **kwargs: Any) -> List[IntegrationV0MessageData]:
        return [
            IntegrationV0MessageData(
                dt=received_at,
                battery=[IntegrationV0MessageCurrentBatteryLevel(voltage=self.packet.sdata_battery_code)],
                consumption=[
                    IntegrationV0MessageConsumption(
                        counter_type=CounterType.COMMON,
                        resource_type=ResourceType.COMMON,
                        channel=1,
                        value=self.packet.sdata_count_ch1_code,
                        overloading_value=None,
                    ),
                    IntegrationV0MessageConsumption(
                        counter_type=CounterType.COMMON,
                        resource_type=ResourceType.COMMON,
                        channel=2,
                        value=self.packet.sdata_count_ch2_code,
                        overloading_value=None,
                    ),
                ],
                temperature=[
                    IntegrationV0MessageCurrentTemperature(value=self.packet.sdata_temperature_code),
                ],
            ),
        ]
