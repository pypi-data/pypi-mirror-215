import base64
from datetime import date, datetime, time
from typing import Dict, Any, List, Tuple, Optional, Union
from uuid import UUID

from api_utils.api_resource.api_response import JsonApiResponsePayload
from api_utils.api_resource.api_response_payload_alias import ApiBaseUserModelPayloadResponse, ApiBaseModelPayloadResponse
from api_utils.internal_api.internal_api import InternalApi
from api_utils.validators.custom_fields import WhiteSpaceStrippedStr, PgTypeInt32, CronScheduleStr
from pydantic import BaseModel, UUID4, Field
from pydantic.types import NonNegativeInt

from data_aggregator_sdk.constants.enums import IntervalSelectValue, EncryptionType, ResourceKind, NetworkTypeEnum, \
    NetworkSysTypeEnum, DeviceHack, DataAggregatorApiUserType, DownlinkTaskType, ScheduleType, ReglamentType, SignalModulation
from data_aggregator_sdk.data_aggregator_api_sdk_config import DataAggregatorApiSdkConfig
from data_aggregator_sdk.integration_message import ProfileKind, ProfileGranulation
from data_aggregator_sdk.types.device import ApiImportDeviceResponse, ApiDataGatewayNetworkDevicePayloadResponse, \
    ApiDeviceMeterPayloadResponse, ApiDeviceChannelPayloadResponse
from data_aggregator_sdk.types.get_data_gateway_network_device_list import ApiDataGatewaysNetworkResponse, \
    ApiDeviceModificationTypeResponse, ApiProtocolResponse
from data_aggregator_sdk.utils.internal_api_error_handler import internal_api_error_handler
from data_aggregator_sdk.utils.internal_api_error_handler_old import internal_api_error_handler_old


class ApiDeviceProfileGranularityResponse(JsonApiResponsePayload):
    device_id: UUID4 = Field(
        ...,
        title="Device ID",
        description="Each device has got unique identifier which is UUID (ex.'f273cbef-0182-4f10-a2b9-17bf54223925')",
    )
    start_date: datetime = Field(
        ...,
        title="Start date of device profile",
        description="Each device profile has start date of collecting data by time granularity",
    )
    end_date: datetime = Field(
        ...,
        title="End date of device profile",
        description="Each device profile has end date of collecting data by time granularity",
    )
    profile_kind: ProfileKind = Field(
        ...,
        title="Type of profile",
        description="Profile type is like side view of collecting data for device (ex. 'VOLTAGE_ABC', 'ENERGY_A_N')",
    )
    granularity_s: ProfileGranulation = Field(
        ...,
        title="Device profile granulation by minutes or seconds",
        description="Granulation is detailing of collecting data, resolution of graph by device (ex. 1 hour (MINUTE_60), 1 second (SECONDS_01))",
    )


class ApiDeviceProfileResponse(JsonApiResponsePayload):
    date_start: datetime = Field(
        ...,
        title="Start date of device profile",
        description="Each device profile has start date of collecting data by time granularity",
    )
    date_end: datetime = Field(
        ...,
        title="End date of device profile",
        description="Each device profile has end date of collecting data by time granularity",
    )
    values_count: int = Field(
        ...,
        title="Amount of collected values",
        description="Number of collected values in sequence of collected values for device by profile type",
    )
    values: List[Optional[float]] = Field(
        ...,
        title="Sequence of collected values",
        description="Collected values for device by profile type looks like sequence of numbers with floating point which depends on profile type",
    )
    profile_kind: ProfileKind = Field(
        ...,
        title="Type of profile",
        description="Profile type is like side view of collecting data for device (ex. 'VOLTAGE_ABC', 'ENERGY_A_N')",
    )
    granularity_s: ProfileGranulation = Field(
        ...,
        title="Device profile granulation by minutes or seconds",
        description="Granulation is detailing of collecting data, resolution of graph by device (ex. 1 hour (MINUTE_60), 1 second (SECONDS_01))",
    )


class DeviceValueDescriptionModelBase(BaseModel):
    registration_date: Optional[datetime]
    kind: ResourceKind = ResourceKind.COMMON_CONSUMED
    tariff_number: int = -1


class DeviceValueDescriptionModel(DeviceValueDescriptionModelBase):
    device_id: Optional[UUID]


class DeviceChannelValueDescriptionModel(DeviceValueDescriptionModelBase):
    device_channel_id: Optional[UUID]


class DeviceMeterValueDescriptionModel(DeviceValueDescriptionModelBase):
    device_meter_id: Optional[UUID]


class ApiDeviceLastValueDateResponse(JsonApiResponsePayload):
    last_value_date: Dict[str, datetime]    # str - UUID (Device.id)


class ApiDeviceChannelLastValueDateResponse(JsonApiResponsePayload):
    last_value_date: Dict[str, datetime]    # str - UUID (DeviceMeter.id)


class ApiDeviceMeterLastValueDateResponse(JsonApiResponsePayload):
    last_value_date: Dict[UUID, datetime]    # str - UUID (DeviceMeter.id)


class GeneralApiDeviceMeter(BaseModel):
    value_multiplier: float
    unit_multiplier: float
    kind: ResourceKind


class GeneralApiDeviceChannel(BaseModel):
    serial_number: int
    inactivity_limit: Optional[int]
    device_meter: List[GeneralApiDeviceMeter]


class ApiDeviceManufacturerResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime

    name: str


class ApiDeviceModificationResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime
    name: Optional[str]
    device_modification_type_id: Optional[UUID4]
    device_modification_type: ApiDeviceModificationTypeResponse


class ApiDataGatewayNetworkDeviceResponse(ApiBaseUserModelPayloadResponse):
    manufacturer_serial_number: str
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    date_produced: Optional[datetime]
    device_manufacturer: ApiDeviceManufacturerResponse
    device_modification: ApiDeviceModificationResponse
    device_channel: List[ApiDeviceChannelPayloadResponse]


class ApiDataGatewayNetworkDeviceByMacAndNetworkPayloadResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime
    uplink_protocol_id: UUID4
    downlink_protocol_id: UUID4
    data_gateway_network_id: UUID4
    mac: int
    key_id: Optional[UUID4]
    device_id: UUID4
    device: ApiDataGatewayNetworkDeviceResponse
    uplink_encryption_key: Optional[str]
    downlink_encryption_key: Optional[str]
    encryption_key: Optional[str]
    protocol: ApiProtocolResponse
    network: Optional[ApiDataGatewaysNetworkResponse]


class DeviceDescriptionModel(BaseModel):
    device_id: Union[UUID4, UUID]
    serial_number: int
    registration_date: Optional[datetime]
    kind: ResourceKind = ResourceKind.COMMON_CONSUMED
    tariff_number: int = -1


class GeneralDeviceValueDescriptionModel(BaseModel):
    device_id: Union[UUID4, UUID]
    serial_number: int
    registration_date: Optional[datetime]
    kind: ResourceKind = ResourceKind.COMMON_CONSUMED
    tariff_number: int = -1


class GeneralDeviceMeterValueDescriptionModel(BaseModel):
    meter_id: UUID
    registration_date: Optional[datetime] = None
    kind: ResourceKind = ResourceKind.COMMON_CONSUMED
    tariff_number: int = -1


class DeviceBatteryLvlDescriptionModel(BaseModel):
    device_id: Union[UUID4, UUID]
    registration_date: Optional[datetime]


class GeneralDeviceValueModel(BaseModel):
    devices: List[GeneralDeviceValueDescriptionModel]


class GeneralDeviceMeterValueModel(BaseModel):
    devices_meter: List[GeneralDeviceMeterValueDescriptionModel]


class GeneralDeviceModificationModel(BaseModel):
    devices: List[DeviceDescriptionModel]


class DeviceValueBatteryLvlModel(BaseModel):
    devices: List[DeviceBatteryLvlDescriptionModel]


class GeneralApiDeviceResponse(BaseModel):
    date: datetime
    device_id: UUID
    serial_number: int
    value: float
    kind: ResourceKind
    tariff_number: int


class GeneralApiDeviceMeterResponse(BaseModel):
    meter_id: UUID
    value: float
    value_date: datetime
    kind: ResourceKind
    tariff_number: int


class GeneralApiDeviceValueResponse(BaseModel):
    device_id: UUID
    serial_number: int
    kind: ResourceKind
    tariff_number: int
    value: float
    value_date: datetime
    last_value: Optional[float]
    last_value_date: Optional[datetime]


class GeneralApiDeviceMeterValueResponse(JsonApiResponsePayload):
    meter_id: UUID
    kind: ResourceKind
    tariff_number: int
    value: float
    value_date: datetime
    last_value: Optional[float]
    last_value_date: Optional[datetime]


class ApiDeviceLowBatteryResponse(JsonApiResponsePayload):
    value_date: datetime
    device_id: UUID
    value: float
    last_value: Optional[float]
    last_value_date: Optional[datetime]


class ApiDeviceResponse(ApiBaseUserModelPayloadResponse):
    manufacturer_serial_number: str
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    date_produced: Optional[datetime]
    device_manufacturer: ApiDeviceManufacturerResponse
    device_modification: ApiDeviceModificationResponse
    device_channel: List[ApiDeviceChannelPayloadResponse]
    data_gateway_network_device: Optional[ApiDataGatewayNetworkDevicePayloadResponse]


class ApiDeviceChannelResponse(BaseModel):
    response: Dict[str, Any]


class ApiDeviceNoData(JsonApiResponsePayload):
    device_id: UUID4
    serial_number: int
    kind: ResourceKind
    tariff_number: int
    last_value: Optional[float]
    last_value_date: Optional[date]
    count_days: int


class ApiDeviceNoDataResponse(JsonApiResponsePayload):
    objects: List[ApiDeviceNoData]
    procent_no_data: float
    count_devices: int
    total_count: int


class ApiDeviceManufacturer(BaseModel):
    manufacturer_serial_number: str


class ApiDeviceFactoryParameters(BaseModel):
    manufacturer_id: Optional[UUID4]
    protocol_id: Optional[UUID4]
    date_produced: Optional[datetime]
    device_modification_type_id: Optional[UUID4]


class ApiDeviceValues(BaseModel):
    devices: List[List[Any]]


class ApiValueDeviceChannelForEripReports(BaseModel):
    devices: List[Tuple[UUID4, int]]
    date_to: datetime


class ApiDeviceEvent(BaseModel):
    devices: List[UUID4]


class ApiDeviceNoDataList(BaseModel):
    devices: List[DeviceDescriptionModel]
    period_from: datetime
    period_to: Optional[datetime]


class ApiUploadDevice(BaseModel):
    device_id: Optional[UUID4]
    manufacturer_name: str
    mac: int
    serial_number: str
    modification_type_name: str
    modification_name: Optional[str]
    date_produced: Optional[datetime]
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    uplink_protocol_id: UUID4
    downlink_protocol_id: UUID4
    key_id: Optional[UUID4]
    uplink_encryption_key: Optional[str]
    downlink_encryption_key: Optional[str]
    data_input_gateway_network_id: UUID4
    data_gateway_id: UUID4


class ApiDataGatewayNetworkDevice(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime
    uplink_protocol_id: UUID4
    downlink_protocol_id: UUID4
    mac: int
    key_id: Optional[UUID4]
    device_id: UUID4
    uplink_encryption_key: Optional[str]
    downlink_encryption_key: Optional[str]
    uplink_encryption_type: EncryptionType
    downlink_encryption_type: EncryptionType
    protocol: ApiProtocolResponse
    network: ApiDataGatewaysNetworkResponse

    @property
    def downlink_encryption_key_bytes(self) -> bytes:
        downlink_encryption_key = self.downlink_encryption_key if self.downlink_encryption_key is not None else ''
        return base64.b64decode(downlink_encryption_key)

    @property
    def uplink_encryption_key_bytes(self) -> bytes:
        uplink_encryption_key = self.uplink_encryption_key if self.uplink_encryption_key is not None else ''
        return base64.b64decode(uplink_encryption_key)


class DeviceData(JsonApiResponsePayload):
    manufacturer_serial_number: str
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    hacks: List[DeviceHack]
    device_tz: Optional[str]
    date_produced: Optional[datetime]
    device_manufacturer: ApiDeviceManufacturerResponse
    device_modification: ApiDeviceModificationResponse
    device_channel: List[ApiDeviceChannelPayloadResponse]
    all_data_gateway_networks: List[ApiDataGatewayNetworkDevice]


class ApiValueDeviceListResponse(JsonApiResponsePayload):
    value_date: datetime
    device_id: UUID4
    serial_number: int
    kind: ResourceKind
    tariff_number: int
    value: float
    last_value: Optional[float]
    last_value_date: Optional[datetime]


class ApiDeviceFirstValueDateResponse(JsonApiResponsePayload):
    date: datetime
    device_id: UUID4
    serial_number: int
    value: float
    kind: ResourceKind
    tariff_number: int


class ApiMeterFirstValueDateResponse(JsonApiResponsePayload):
    meter_id: UUID
    value: float
    value_date: datetime
    kind: ResourceKind
    tariff_number: int


class ApiLastValueEripReportsResponse(JsonApiResponsePayload):
    device_id: UUID4
    serial_number: int
    date: str
    value: float
    kind: ResourceKind
    tariff_number: int


class DeviceMac(JsonApiResponsePayload):
    mac: int
    device_id: UUID4
    address_id: UUID4


class DeviceImbalanceObject(JsonApiResponsePayload):
    object_procent: float
    different: float
    flat_sum: float
    group_sum: float
    group_devices: List[DeviceMac]
    count_not_data_flat: int
    all_flat_count: int
    address_id: UUID4


class ApiImbalanceValueDeviceListResponse(JsonApiResponsePayload):
    procent: float
    imbalance: float
    object: List[DeviceImbalanceObject]


class SelectValueResultObject(JsonApiResponsePayload):
    number_object: Optional[str]
    count_flat_devices: Optional[int]
    count_not_data_flat: Optional[int]
    device_id: List[UUID4]
    last_date: date
    previous_last_value: float
    current_last_value: float
    address_flat_node_id: Optional[str]
    mac: Optional[int]


class ApiObjectValuesDeviceListResponse(JsonApiResponsePayload):
    count_object_devices: int
    count_not_data_objects_devices: int
    objects: List[SelectValueResultObject]


class DeviceEventsResponse(BaseModel):
    event_id: UUID4
    date_created: str
    user_created_id: UUID4
    value: Optional[float]
    device_id: UUID4
    serial_number: Optional[int]
    type: str
    date: str
    data: Optional[Dict[str, Any]]
    is_system_generated: bool


class DeviceStateSyncDataResponse(JsonApiResponsePayload):
    device_events: List[DeviceEventsResponse]
    offset_id: Optional[UUID4]


class UpdateSyncOffsetResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    date_modified: datetime
    user_created_id: UUID4
    user_modified_id: UUID4
    api_user_id: UUID4
    type: str
    offset: datetime
    is_confirmed: bool


class ApiModificationResponse(BaseModel):
    sys_name: str
    name_ru: str
    name_en: str


class ApiModificationResponseForDevices(JsonApiResponsePayload):
    device_modification: Dict[str, ApiModificationResponse]


class ApiLastValueDateResponseForDevices(JsonApiResponsePayload):
    last_value_date: Dict[str, datetime]


class ApiDeviceImbalanceModel(BaseModel):
    flat_devices: Optional[List[List[Any]]]
    group_devices: Optional[List[List[Any]]]


class ApiBinaryDataResponse(JsonApiResponsePayload):
    id: UUID4
    date_created: datetime
    user_created_id: UUID4
    hash: str
    content: str
    file_name: str


class BaseApiBSDownlinkTask(JsonApiResponsePayload):
    note: WhiteSpaceStrippedStr
    type: DownlinkTaskType
    priority: PgTypeInt32
    broadcast: bool
    schedule_type: ScheduleType
    schedule_effective_date_from: datetime
    schedule_effective_date_to: datetime
    reglament_type: ReglamentType
    signal_power: int
    signal_freq: int
    signal_baudrate: int
    signal_modulation: SignalModulation
    lbt_enable: bool
    lbt_max_waiting_time_ms: int
    lbt_silent_time_ms: int
    force: bool
    retry_count: NonNegativeInt
    retry_min_delay_ms: int
    min_tx_delay_after_rx_ms: Optional[int]
    tx_duration_ms: Optional[int]


class ApiBSDownlinkTaskResponse(BaseApiBSDownlinkTask):
    id: UUID4
    date_created: datetime
    user_created_id: UUID4
    schedule_time: Optional[list[time]]
    schedule_cron: Optional[list[CronScheduleStr]]
    bs_downlink_task_time_sync_id: Optional[UUID4]
    bs_downlink_task_firmware_update_id: Optional[UUID4]
    bs_downlink_task_unbp_message_id: Optional[UUID4]


class ApiDataGatewayNetworkResponse(ApiBaseUserModelPayloadResponse):
    name: str
    type_network: NetworkTypeEnum
    data_gateway_id: UUID4
    sys_type: NetworkSysTypeEnum
    specifier: Optional[str]
    params: Optional[Dict[str, Any]]


class DataAggregatorApiUserResponse(ApiBaseModelPayloadResponse):
    date_expiration: datetime
    name: str
    note: str
    permissions: List[int]
    type: DataAggregatorApiUserType
    data_gateway_network_id: Optional[UUID]
    data_gateway_network: Optional[ApiDataGatewayNetworkResponse]


class DataAggregatorApiSdk:

    def __init__(self, config: DataAggregatorApiSdkConfig) -> None:
        self._config = config
        self._api = InternalApi(entry_point=self._config.api_url, default_auth_token=self._config.api_token)
        self._api_device = InternalApi(entry_point=self._config.api_device_url, default_auth_token=self._config.api_token)

        self._api_base_station: Optional[InternalApi] = None
        if self._config.api_base_station_url is not None:
            self._api_base_station = InternalApi(entry_point=self._config.api_base_station_url, default_auth_token=self._config.api_token)

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_device_dict_by_mac_and_network(self, mac: str, gateway_id: UUID, network_id: UUID) -> Dict[str, Any]:  # TODO: typing
#         return self._api_device.request_get(f'/data-gateways/{gateway_id}/networks/{network_id}/device_mac/{mac}').check().payload_raw    # type: ignore

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_device_data(self, gateway_id: UUID, network_id: UUID, mac: int) -> DeviceData:
#         return self._api_device.request_get(f'/data-gateways/{gateway_id}/networks/{network_id}/device_mac/{mac}/data')\
#             .typed(DeviceData).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_devices_data(self, gateway_id: UUID, network_id: UUID, mac_list: List[int]) -> List[DeviceData]:
        return self._api_device.request_post(f'/data-gateways/{gateway_id}/networks/{network_id}/data', json={"mac_list": mac_list})\
            .typed(List[DeviceData]).check().payload

    '''used in services: Service Data Gateway'''
    @internal_api_error_handler
    def get_device(self, device_id: UUID) -> ApiDeviceResponse:
        return self._api_device.request_get(f'/devices/{device_id}').typed(ApiDeviceResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_device_channels(self, device_id: UUID) -> List[ApiDeviceChannelPayloadResponse]:
        return self._api_device.request_get(f'/device/{device_id}/device_channel/').typed(List[ApiDeviceChannelPayloadResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_device_meters(self, device_channel_id: UUID) -> List[ApiDeviceMeterPayloadResponse]:
        return self._api_device.request_get(f'/device-channel/{device_channel_id}/device-meter').typed(List[ApiDeviceMeterPayloadResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def update_device_meter_unit_multiplier(
        self,
        device_meter_id: UUID,
        device_channel_id: UUID,
        unit_multiplier: float,
        date_application_from: Optional[date],
        date_application_to: Optional[date],
    ) -> ApiDeviceMeterPayloadResponse:
        return self._api_device.request_put(
            f'/device-channel/{device_channel_id}/device-meter/{device_meter_id}/unit-multiplier',
            json={
                "unit_multiplier": unit_multiplier,
                "date_application_from": date_application_from,
                "date_application_to": date_application_to,
            },
        ).typed(ApiDeviceMeterPayloadResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_or_create_channel(
        self,
        device_id: UUID,
        serial_number: int,
        inactivity_limit: Optional[int],
    ) -> ApiDeviceChannelPayloadResponse:
        return self._api_device.request_post('/device_channel', json={
            "device_id": str(device_id),
            "serial_number": serial_number,
            "inactivity_limit": inactivity_limit,
        }).typed(ApiDeviceChannelPayloadResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_or_create_meter(
        self,
        device_channel_id: UUID,
        value_multiplier: Optional[float],
        unit_multiplier: Optional[float],
    ) -> ApiDeviceMeterPayloadResponse:
        return self._api_device.request_post('/device-meter', json={
            device_channel_id: str(device_channel_id),
            value_multiplier: value_multiplier,
            unit_multiplier: unit_multiplier,
        }).typed(ApiDeviceMeterPayloadResponse).check().payload

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_device_networks(
#         self,
#         device_id: UUID,
#         type_network: NetworkTypeEnum,
#         limit: Optional[int],
#         offset: Optional[int],
#         filters: Optional[List[Dict[str, Any]]],
#         sorts: Optional[List[Tuple[str, str]]],
#     ) -> List[Dict[str, Any]]:  # TODO: typing
#         if type_network not in NetworkTypeEnum:
#             raise ValueError("NetworkType can be only input or output")
#         return self._api_device.request_get(f'/device-network/{device_id}/type/{type_network.value}', q={
#             "filters": filters,
#             "sorts": sorts,
#             "limit": limit,
#             "offset": offset,
#         }).check().payload_raw    # type: ignore

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_device_manufacturers(
        self,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> List[ApiDeviceManufacturerResponse]:
        return self._api_device.request_get(
            '/manufacturers',
            q={
                "filters": filters,
                "sorts": sorts,
                "limit": limit,
                "offset": offset,
            }).typed(List[ApiDeviceManufacturerResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_protocols(
        self,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> List[ApiProtocolResponse]:
        return self._api_device.request_get(
            '/protocols',
            q={"filters": filters, "sorts": sorts, "limit": limit, "offset": offset},
        ).typed(List[ApiProtocolResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_device_modification_types(
        self,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> List[ApiDeviceModificationTypeResponse]:
        return self._api_device.request_get(
            '/device-modification-types',
            q={"filters": filters, "sorts": sorts, "limit": limit, "offset": offset},
        ).typed(List[ApiDeviceModificationTypeResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_device_factory_parameters(self, devices_id: Union[UUID, List[UUID]]) -> List[ApiDeviceResponse]:
        devices = [devices_id] if not isinstance(devices_id, list) else devices_id
        return self._api_device.request_post(
            '/devices/factory-parameters',
            json={"devices": [str(device) for device in devices]},
        ).typed(List[ApiDeviceResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler_old
    def get_device_short_factory_parameters(self, device_ids: Union[UUID, List[UUID]]) -> Dict[str, Any]:  # TODO: typing
        devices = [device_ids] if not isinstance(device_ids, list) else device_ids
        return self._api_device.request_post(
            '/devices/short-factory-parameters',
            json={"devices": devices},
        ).check().payload_raw    # type: ignore

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def update_device_manufacturer_by_id(self, device_id: UUID, manufacturer_serial_number: str) -> ApiDeviceResponse:
        return self._api_device.request_patch(
            f'/devices/{device_id}/serial_number',
            json={'manufacturer_serial_number': manufacturer_serial_number},
        ).typed(ApiDeviceResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def update_device_factory_parameters(
        self,
        device_id: UUID,
        manufacturer_id: Optional[UUID],
        protocol_id: Optional[UUID],
        date_produced: Optional[datetime],
        device_modification_id: Optional[UUID],
        device_modification_type_id: Optional[UUID],
    ) -> ApiDeviceResponse:
        body_data: Dict[str, Any] = {'date_produced': str(date_produced) if date_produced else None}
        if manufacturer_id is not None:
            body_data.update({'manufacturer_id': str(manufacturer_id)})

        if protocol_id is not None:
            body_data.update({'protocol_id': str(protocol_id)})

        if device_modification_id is not None:
            body_data.update({'device_modification_id': device_modification_id})

        if device_modification_type_id is not None:
            body_data.update({'device_modification_type_id': str(device_modification_type_id)})

        return self._api_device.request_patch(
            f'/device/{device_id}/factory-parameters',
            json=body_data,
        ).typed(ApiDeviceResponse).check().payload

#   '''used in services: not used'''
#     @internal_api_error_handler
#     def get_device_logger_data(
#         self,
#         device_id: UUID,
#     ) -> Dict[str, Any]:  # TODO: typing
#         return self._api_device.request_get(
#             f'/devices/{device_id}/logger_data').check().payload_raw    # type: ignore

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_value_for_device_list(
        self,
        period_from: date | datetime,
        period_to: date | datetime,
        iteration_interval: Optional[IntervalSelectValue],
        devices: GeneralDeviceValueModel,
        locf: Optional[bool],
    ) -> List[ApiValueDeviceListResponse]:
        return self._api.request_post('/list-device/value-for-device-list', json=devices, q={
            'period_from': period_from,
            'period_to': period_to,
            'locf': locf,
            'iteration_interval': iteration_interval.value if iteration_interval is not None else None,
        }).typed(List[ApiValueDeviceListResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_value_for_device_meter(
        self,
        period_from: date | datetime,
        period_to: date | datetime,
        iteration_interval: Optional[IntervalSelectValue],
        devices_meter: GeneralDeviceMeterValueModel,
    ) -> List[GeneralApiDeviceMeterValueResponse]:
        return self._api.request_post('/list-device/value-for-devices-meter', json=devices_meter, q={
            'period_from': period_from,
            'period_to': period_to,
            'iteration_interval': iteration_interval.value if iteration_interval is not None else None,
        }).typed(List[GeneralApiDeviceMeterValueResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_battery_lvl_for_device_list(
        self,
        period_from: date,
        period_to: date,
        iteration_interval: Optional[IntervalSelectValue],
        devices: DeviceValueBatteryLvlModel,
        locf: Optional[bool],
    ) -> List[ApiDeviceLowBatteryResponse]:
        return self._api.request_post('/list-device/battery-lvl-for-device-list', json=devices, q={
            'period_from': period_from,
            'period_to': period_to,
            'locf': locf,
            'iteration_interval': iteration_interval.value if iteration_interval is not None else None,
        }).typed(List[ApiDeviceLowBatteryResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_first_value_date_for_devices(
        self,
        devices: GeneralDeviceValueModel,
    ) -> List[ApiDeviceFirstValueDateResponse]:
        return self._api.request_post(
            '/list-device/search-first-value-date',
            json=devices,
        ).typed(List[ApiDeviceFirstValueDateResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_first_value_date_for_meters(
        self,
        meters: GeneralDeviceMeterValueModel,
    ) -> List[ApiMeterFirstValueDateResponse]:
        return self._api.request_post(
            '/meters/first-value-date',
            json=meters,
        ).typed(List[ApiMeterFirstValueDateResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_last_value_for_erip_reports(
        self,
        devices: List[Tuple[UUID4, int]],
        date_to: datetime,
    ) -> List[ApiLastValueEripReportsResponse]:
        # devices = List[List['device_id: UUID', serial_number: int]]
        return self._api.request_post(
            '/erip-reports/last-value',
            json=ApiValueDeviceChannelForEripReports(date_to=date_to, devices=devices),
        ).typed(List[ApiLastValueEripReportsResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_object_values_by_device_list(
        self,
        devices: Dict[str, List[List[Any]]],
        reporting_period: date,
    ) -> List[ApiObjectValuesDeviceListResponse]:
        # Dict["name_object": List[List['device_id: UUID', channel: int]],
        # "name_object": List[List['device_id: UUID', channel: int]]]
        return self._api.request_post(
            '/list-device/value-object-period',
            q={'reporting_period': reporting_period},
            json={'devices': devices},
        ).typed(List[ApiObjectValuesDeviceListResponse]).check().payload

#   '''used in services: not used'''
# Сделан с соответствием с новой концепцией насчет DataAggregator (get_object_values_by_device_list)
#     @internal_api_error_handler
#     def get_consumption_period_by_device_list(self, devices: List[List[Any]], reporting_period: date) -> List[Dict[str, Any]]:  # TODO: typing
#         # List[List['device_id: UUID', channel: int]]
#         return self._api.request_post('/list-device/consumption-period', q={'reporting_period': reporting_period}, json={'devices': devices}).check().payload_raw

#   '''used in services: not used'''
#     @internal_api_error_handler
#     def get_object_delta(self, devices: Dict[str, List[List[Any]]]) -> List[Dict[str, Any]]:  # TODO: typing
#         # Dict["name_object": List[List['device_id: UUID', channel: int]],
#         # "name_object": List[List['device_id: UUID', channel: int]]]
#         return self._api.request_post('/list-device/value-delta', json={'devices': devices}).check().payload_raw    # type: ignore

#   '''used in services: not used'''
#     @internal_api_error_handler
#     def get_obj_values_deltas_for_group_devices(
#         self,
#         devices_info_box: TDevicesInfoBox,
#         period_from: datetime,
#         period_to: datetime,
#         limit: int,
#         offset: int,
#     ) -> List[Dict[str, Any]]:  # TODO: typing
#         return self._api.request_post('/devices/group/values-deltas', json={"devices_info_box": devices_info_box_to_json(devices_info_box)}, q=get_query_params(
#             period_from=period_from,
#             period_to=period_to,
#             limit=limit,
#             offset=offset,
#         )).check().payload_raw    # type: ignore

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_object_imbalance_by_period(
        self,
        devices: Dict[str, ApiDeviceImbalanceModel],
        period_from: date,
        period_to: date,
    ) -> List[ApiImbalanceValueDeviceListResponse]:
        # Dict["object_id": Dict[
        # "flat_devices":List[List['device_id: UUID', channel: int]],
        # "group_devices":List[List['device_id: UUID', channel: int]]]]
        return self._api.request_post(
            '/list-device/imbalance',
            q={'period_from': period_from, 'period_to': period_to},
            json={'devices': devices},
        ).typed(List[ApiImbalanceValueDeviceListResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_object_actual_imbalance_by_period(
        self,
        devices: Dict[str, ApiDeviceImbalanceModel],
        period_from: date,
        period_to: date,
    ) -> List[ApiImbalanceValueDeviceListResponse]:
        # Dict["object_id": Dict[
        # "flat_devices":List[List['device_id: UUID', channel: int]],
        # "group_devices":List[List['device_id: UUID', channel: int]]]]
        return self._api.request_post(
            '/list-device/imbalance/actual',
            q={'period_from': period_from, 'period_to': period_to},
            json={'devices': devices},
        ).typed(List[ApiImbalanceValueDeviceListResponse]).check().payload

#   '''used in services: not used'''
#     @internal_api_error_handler
#     def get_graphics_object_imbalance_by_period(
#         self,
#         devices: Dict[str, List[List[Any]]],
#         period_from: date,
#         period_to: date,
#     ) -> Dict[str, Any]:  # TODO: typing
#         # Dict["name_object": List[List['object_id': UUID]],
#         # "group_devices":List[List['device_id: UUID', channel: int]],
#         # "flat_devices":List[List['device_id: UUID', channel: int]]}
#         return self._api.request_post(
#             '/list-device/imbalance-graphics',
#             q={'period_from': period_from, 'period_to': period_to},
#             json={'devices': devices},
#         ).check().payload_raw    # type: ignore

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_events_magnet_devices(
#         self,
#         devices: List[UUID],
#         period_from: date,
#         period_to: date,
#     ) -> Dict[str, Any]:  # TODO: typing
#         return self._api.request_post(
#             '/events-magnet/devices',
#             q={'period_from': period_from, 'period_to': period_to},
#             json=ApiDeviceEvent(devices=devices),
#         ).check().payload_raw    # type: ignore

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_events_low_battery_devices(
#         self,
#         devices: List[UUID],
#         period_from: date,
#         period_to: date,
#     ) -> Dict[str, Any]:  # TODO: typing
#         return self._api.request_post(
#             '/events-battery/devices',
#             q={'period_from': period_from, 'period_to': period_to},
#             json=ApiDeviceEvent(devices=devices),
#         ).check().payload_raw    # type: ignore

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_events_devices(
#         self,
#         devices: List[UUID],
#         period_from: date,
#         period_to: date,
#     ) -> Dict[str, Any]:  # TODO: typing
#         return self._api.request_post(
#             '/events/devices',
#             q={'period_from': period_from, 'period_to': period_to},
#             json=ApiDeviceEvent(devices=devices),
#         ).check().payload_raw    # type: ignore

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_devices_not_data(
        self,
        devices: ApiDeviceNoDataList,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> ApiDeviceNoDataResponse:
        query_params: Dict[str, Any] = {
            "filter": filters,
            "sort": sorts,
            "limit": limit,
            "offset": offset,
        }
        return self._api.request_post(
            '/devices/no-data',
            q=query_params,
            json=devices,
        ).typed(ApiDeviceNoDataResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def upload_device(
        self,
        device_id: Optional[UUID],
        manufacturer_name: str,
        mac: int,
        manufacturer_serial_number: str,
        modification_type_id: str,
        modification_id: Optional[str],
        date_produced: Optional[datetime],
        firmware_version: Optional[str],
        hardware_version: Optional[str],
        uplink_protocol_id: UUID,
        downlink_protocol_id: UUID,
        key_id: Optional[UUID],
        uplink_encryption_key: Optional[str],
        downlink_encryption_key: Optional[str],
        uplink_encryption_type: EncryptionType,
        downlink_encryption_type: EncryptionType,
        data_input_gateway_network_id: UUID,
        data_gateway_id: UUID,
        device_channels: List[GeneralApiDeviceChannel],
        modification_name: Optional[str],  # for script
        modification_type_name: Optional[str],  # for script
    ) -> ApiImportDeviceResponse:
        return self._api_device.request_post('/import/devices', json={
            'device_id': str(device_id) if device_id is not None else None,
            'manufacturer_name': manufacturer_name,
            'mac': mac,
            'manufacturer_serial_number': manufacturer_serial_number,
            'modification_type_id': modification_type_id,
            'modification_id': modification_id,
            'date_produced': str(date_produced) if date_produced is not None else None,
            'firmware_version': firmware_version,
            'hardware_version': hardware_version,
            'uplink_protocol_id': str(uplink_protocol_id) if uplink_protocol_id is not None else None,
            'downlink_protocol_id': str(downlink_protocol_id) if downlink_protocol_id is not None else None,
            'key_id': str(key_id) if key_id is not None else None,
            'uplink_encryption_key': uplink_encryption_key,
            'downlink_encryption_key': downlink_encryption_key,
            'uplink_encryption_type': uplink_encryption_type,
            'downlink_encryption_type': downlink_encryption_type,
            'data_input_gateway_network_id': str(data_input_gateway_network_id),
            'data_gateway_id': str(data_gateway_id),
            'device_channels': device_channels,
            'modification_name': modification_name,
            'modification_type_name': modification_type_name,
        }).typed(ApiImportDeviceResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_events_to_sync_api_user_data(self) -> DeviceStateSyncDataResponse:
        return self._api.request_get('/device-state-sync/events').typed(DeviceStateSyncDataResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def update_device_state_sync_offset(self, sync_offset_id: UUID, is_confirmed: bool = True) -> UpdateSyncOffsetResponse:
        return self._api.request_patch(f'/device-state-sync-offset/{str(sync_offset_id)}', json={'is_confirmed': is_confirmed}).typed(UpdateSyncOffsetResponse).check().payload

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_base_station_by_token(self, api_token: Optional[Tuple[Optional[str], str]]) -> Dict[str, Any]:  # TODO: typing
#         assert self._api_base_station is not None
#         return self._api_base_station.request_get('/base-station').check().payload_raw    # type: ignore

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_modifications_for_list_devices(self, devices: GeneralDeviceValueModel) -> ApiModificationResponseForDevices:
        return self._api_device.request_post(
            '/device-modifications/list-devices',
            json=devices,
        ).typed(ApiModificationResponseForDevices).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_last_value_date_by_device(
        self,
        device: DeviceValueDescriptionModel,
        period_selection: Optional[date],
        period_to: Optional[datetime],
    ) -> ApiDeviceLastValueDateResponse:
        return self._api_device.request_post(
            '/device/last-value-date',
            json=device,
            q={"period_selection": period_selection, "period_to": period_to},
        ).typed(ApiDeviceLastValueDateResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_last_value_date_by_device_channel(
        self,
        device_channel: DeviceChannelValueDescriptionModel,
        period_selection: Optional[date],
        period_to: Optional[datetime],
    ) -> ApiDeviceChannelLastValueDateResponse:
        return self._api_device.request_post(
            '/device-channel/last-value-date',
            json=device_channel,
            q={"period_selection": period_selection, "period_to": period_to},
        ).typed(ApiDeviceChannelLastValueDateResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_last_value_date_for_list_devices(
        self,
        devices: GeneralDeviceValueModel,
        period_selection: Optional[date],
        period_to: Optional[datetime],
    ) -> ApiLastValueDateResponseForDevices:
        return self._api_device.request_post(
            '/device-channel/last-value-date/list-devices',
            json=devices,
            q={"period_selection": period_selection, "period_to": period_to},
        ).typed(ApiLastValueDateResponseForDevices).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_last_value_date_by_device_meter_list(
        self,
        device_meters: GeneralDeviceMeterValueModel,
        period_selection: Optional[date],
        period_to: Optional[datetime],
    ) -> ApiDeviceMeterLastValueDateResponse:
        return self._api_device.request_post(
            '/device-meter/last-value-date/list-meters',
            json=device_meters,
            q={"period_selection": period_selection, "period_to": period_to},
        ).typed(ApiDeviceMeterLastValueDateResponse).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_last_value_date_by_device_meter(
        self,
        device_meter: DeviceMeterValueDescriptionModel,
        period_selection: Optional[date],
        period_to: Optional[datetime],
    ) -> ApiDeviceMeterLastValueDateResponse:
        return self._api_device.request_post(
            '/device-meter/last-value-date',
            json=device_meter,
            q={"period_selection": period_selection, "period_to": period_to},
        ).typed(ApiDeviceMeterLastValueDateResponse).check().payload

    '''used in services: Iot Account Application Backend, Service Data Gateway'''
    @internal_api_error_handler
    def get_data_gateway_networks(
        self,
        data_gateway_id: UUID,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> List[ApiDataGatewayNetworkResponse]:
        query_params: Dict[str, Any] = {
            "filter": filters,
            "sort": sorts,
        }
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset
        return self._api_device.request_get(
            f'/data-gateways/{data_gateway_id}/networks',
            q=query_params,
        ).typed(List[ApiDataGatewayNetworkResponse]).check().payload

    '''used in services: Iot Account Application Backend'''
    @internal_api_error_handler
    def get_device_modifications(
        self,
        limit: Optional[int],
        offset: Optional[int],
        filters: Optional[List[Dict[str, Any]]],
        sorts: Optional[List[Tuple[str, str]]],
    ) -> List[ApiDeviceModificationResponse]:
        query_params: Dict[str, Any] = {
            "filter": filters,
            "sort": sorts,
        }
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset
        return self._api_device.request_get('/device-modifications', q=query_params).typed(List[ApiDeviceModificationResponse]).check().payload

    '''used in services: Iot Account Application Gateway, Service Data Gateway'''
    @internal_api_error_handler
    def get_device_profiles_granularity_list_by_device_id(
        self,
        device_id: UUID,
        date_from: Optional[datetime],
        date_to: Optional[datetime],
        profile_kinds: Optional[str],
    ) -> List[ApiDeviceProfileGranularityResponse]:
        query: Dict[str, Any] = {"date_from": date_from, "date_to": date_to}
        if profile_kinds:
            query.update({"profile_kinds": profile_kinds})
        return self._api.request_get(
            f'/device-profiles/{device_id}/granularity',
            q=query,
        ).typed(List[ApiDeviceProfileGranularityResponse]).check().payload

    '''used in services: Iot Account Application Gateway, Service Data Gateway'''
    @internal_api_error_handler
    def get_device_profiles_list(
        self,
        device_id: UUID,
        granularity_s: Optional[str],
        profile_kinds: Optional[str],
        dt_from: datetime,
        dt_to: datetime,
    ) -> List[ApiDeviceProfileResponse]:
        query: Dict[str, Any] = {"dt_from": dt_from, "dt_to": dt_to}
        if profile_kinds:
            query.update({"profile_kinds": profile_kinds})
        if granularity_s:
            query.update({"granularity_s": granularity_s})
        return self._api.request_get(
            f'/device-profiles/{device_id}',
            q=query,
        ).typed(List[ApiDeviceProfileResponse]).check().payload

    @internal_api_error_handler
    def get_bs_downlink_tasks(
        self,
    ) -> List[ApiBSDownlinkTaskResponse]:
        assert self._api_base_station is not None
        return self._api_base_station.request_get(
            '/bs-downlink-tasks',
        ).typed(List[ApiBSDownlinkTaskResponse]).check().payload

    @internal_api_error_handler
    def get_bs_downlink_task_by_id(
        self,
        task_id: UUID,
    ) -> ApiBSDownlinkTaskResponse:
        assert self._api_base_station is not None
        return self._api_base_station.request_get(
            f'/bs-downlink-tasks/{task_id}',
        ).typed(ApiBSDownlinkTaskResponse).check().payload

    @internal_api_error_handler
    def get_binary_data_list(
        self,
    ) -> List[ApiBinaryDataResponse]:
        assert self._api_base_station is not None
        return self._api_base_station.request_get(
            '/binary-data',
        ).typed(List[ApiBinaryDataResponse]).check().payload

    @internal_api_error_handler
    def get_binary_data_by_id(
        self,
        binary_data_id: UUID,
    ) -> ApiBinaryDataResponse:
        assert self._api_base_station is not None
        return self._api_base_station.request_get(
            f'/binary-data/{binary_data_id}',
        ).typed(ApiBinaryDataResponse).check().payload

#     '''used in services: not used'''
#     @internal_api_error_handler
#     def get_data_gateway_netowork_device_list(
#         self,
#         gateway_id: UUID,
#         devices: List[ApiDataGatewayNetworkDevicesInfo],
#         limit: Optional[int],
#         offset: Optional[int],
#         filters: Optional[List[Dict[str, Any]]],
#         sorts: Optional[List[Tuple[str, str]]],
#     ) -> InternalApiResponse[List[ApiDataGatewayNetworkDeviceInfoResponse]]:        # type: ignore
#         query_params: Dict[str, Any] = {
#             "filter": filters,
#             "sort": sorts,
#         }
#         if limit is not None:
#             query_params['limit'] = limit
#         if offset is not None:
#             query_params['offset'] = offset
#         return self._api_device.request_post(
#             f'/data-gateways/{gateway_id}/devices',
#             q=query_params,
#             json=json.dumps(ApiDataGatewayNetworkDevicesBody(devices=devices).dict()),
#         ).typed(List[ApiDataGatewayNetworkDeviceInfoResponse]).check()

    '''used in services: Iot Account Application Gateway, Service Data Gateway'''
    @internal_api_error_handler
    def get_data_aggregator_api_user(
        self,
        api_user_id: UUID,
    ) -> DataAggregatorApiUserResponse:
        return self._api.request_get(
            f'/api-user/{api_user_id}',
        ).typed(DataAggregatorApiUserResponse).check().payload
