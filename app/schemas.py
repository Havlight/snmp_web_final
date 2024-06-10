from ninja import Schema


class Error(Schema):
    message: str


class Success(Schema):
    message: str


class MacTableSchema(Schema):
    mac: str
    port: int
    status: int


class GenericMibResultSchema(Schema):
    # mib: str
    oid: str
    value: str


class PortWarningSchema(Schema):
    port: int
    status: str


class PortRateSchema(Schema):
    port: str
    in_rate: float
    out_rate: float


class PortError(Schema):
    port: int
    error_diff: int
    error_rate: float


class VlanIn(Schema):
    id: int
    name: str
    ports: list[int]
